from __future__ import annotations

from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy

from accounts.models import User
from helpdesk.utils import get_object_or_none


class TicketQueue(models.Model):
    name = models.CharField("Ticket Queue Name", max_length=32)
    slug = models.SlugField("Slug", max_length=32, unique=True)
    description = models.CharField("Description", max_length=100)
    display_priority = models.PositiveSmallIntegerField("Display Priority", default=1)
    show_in_overview = models.BooleanField("Show in Display Overview", default=True)
    escalation_queue = models.ForeignKey(
        "tickets.TicketQueue",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="escalates_to",
        related_query_name="escalates_to",
    )

    class Meta:
        ordering = ["-display_priority", "name"]

    def __str__(self) -> str:
        if self.description:
            return f"{self.name} - {self.description}"
        return self.name

    def attention_count(self) -> int:
        tickets = self.tickets.with_event_fields().exclude(
            models.Q(status=TicketStatus.RESOLVED) | models.Q(assignee_id__isnull=False),
        )
        return tickets.count()

    def in_progress_count(self) -> int:
        tickets = self.tickets.with_event_fields().filter(
            status=TicketStatus.OPEN,
            assignee_id__isnull=False,
        )
        return tickets.count()


class TicketQuerySet(models.QuerySet["Ticket"]):
    def with_status(self) -> TicketQuerySet:
        events = (
            TicketEvent.objects.exclude(new_status__exact="")
            .filter(
                ticket_id=models.OuterRef("pk"),
            )
            .order_by("-created_at")
        )
        return self.annotate(status=models.Subquery(events.values("new_status")[:1]))

    def with_assignee(self) -> TicketQuerySet:
        events = (
            TicketEvent.objects.annotate(
                assignee=models.F("assignee_change__user"),
            )
            .filter(
                ticket_id=models.OuterRef("pk"),
                assignee_change__isnull=False,
            )
            .order_by("-created_at")
        )
        return self.annotate(assignee_id=models.Subquery(events.values("assignee")[:1]))

    def with_event_fields(self) -> TicketQuerySet:
        return self.with_assignee().with_status()


class TicketManager(models.Manager):
    def get_queryset(self) -> TicketQuerySet:  # type: ignore[override]
        return TicketQuerySet(self.model, using=self._db)

    def with_event_fields(self) -> TicketQuerySet:
        return self.get_queryset().with_event_fields()


class Ticket(models.Model):
    title = models.CharField(max_length=120)
    queue = models.ForeignKey(
        TicketQueue,
        on_delete=models.PROTECT,
        related_name="tickets",
        related_query_name="tickets",
    )

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.PROTECT,
        related_name="tickets",
        related_query_name="tickets",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TicketManager()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"#{self.id} - {self.title}"

    def get_absolute_url(self) -> str:
        return reverse_lazy("tickets:ticket_detail", kwargs={"pk": self.id})

    @property
    def assignee(self) -> User | None:
        """
        Get the assignee of this ticket.

        Must be called only when the Ticket has with_event_fields()
        """
        return get_object_or_none(User, pk=self.assignee_id)  # type: ignore[attr-defined]

    @property
    def status_name(self) -> str:
        """
        Get the name of the status.

        Must be called only when the Ticket has with_event_fields()
        """
        lookups = dict(TicketStatus.choices)
        return lookups.get(self.status, "Unknown")  # type: ignore[attr-defined]

    @property
    def status_css_tag(self) -> str:
        """
        Get the CSS class of the status.

        Must be called only when the Ticket has with_event_fields()
        """
        lookup = {
            TicketStatus.RESOLVED: "is-info",
            TicketStatus.OPEN: "is-primary",
        }
        return lookup.get(self.status, "is-primary")  # type: ignore[attr-defined]

    @property
    def is_escalatable(self) -> bool:
        return self.queue.escalation_queue is not None

    @property
    def last_updated(self) -> datetime:
        return max(self.updated_at, self.created_at, *self.events.values_list("created_at", flat=True))


class TicketStatus(models.TextChoices):
    OPEN = "OP", "Open"
    RESOLVED = "RS", "Resolved"


class TicketEventAssigneeChange(models.Model):
    """
    For a given ticket event, this model exists iff the assignee changed.

    We need a separate table for this so that we can differentiate
    between changing of an assignee and removal.

    One instance of this model exists per user.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        if self.user:
            return f"Assignee changed to {self.user}"
        else:
            return "Unassigned"


class TicketEvent(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="events",
        related_query_name="events",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
    )
    new_status = models.CharField(  # noqa: DJ001
        verbose_name="Updated status",
        help_text="If the event changes the state of the ticket, enter it here.",
        max_length=2,
        choices=TicketStatus.choices,
        blank=True,
    )
    assignee_change = models.ForeignKey(
        TicketEventAssigneeChange,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    ~models.Q(new_status__exact="")
                    | ~models.Q(comment__exact="")
                    | models.Q(assignee_change__isnull=False),
                ),
                name="valid_event",
            ),
        ]

    def __str__(self) -> str:
        return f"Event on #{self.ticket.id} at {self.created_at} by {self.user}"

    def clean(self) -> None:
        """Ensure that an event has at least a comment or status change."""
        if not (self.new_status or self.comment or self.assignee_change):
            raise ValidationError("Please provide at least a status update or comment.")
