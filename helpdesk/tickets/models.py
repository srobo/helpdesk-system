from __future__ import annotations

from django.db import models
from django.urls import reverse_lazy


class TicketQueue(models.Model):
    name = models.CharField("Ticket Queue Name", max_length=32)
    slug = models.SlugField("Slug", max_length=32)
    display_priority = models.PositiveSmallIntegerField("Display Priority", default=1)
    escalation_queue = models.ForeignKey(
        'tickets.TicketQueue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalates_to',
        related_query_name='escalates_to',
    )

    class Meta:
        ordering = ["-display_priority", "name"]

    def __str__(self) -> str:
        return f"Ticket Queue: {self.name}"


class Ticket(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
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

    opened_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="opened_tickets",
        related_query_name="opened_tickets",
    )
    assignee = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tickets",
        related_query_name="tickets",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"#{self.id} - {self.title}"

    def get_absolute_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={'pk': self.id})

    @property
    def is_escalatable(self) -> bool:
        return self.queue.escalation_queue is not None


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comments",
    )
    content = models.TextField()
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="comments",
        related_query_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment on #{self.ticket.id} at {self.created_at} by {self.author}"


class TicketResolution(models.Model):

    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="resolution",
        related_query_name="resolution",
    )
    comment = models.TextField(blank=True)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
    )
    resolved_at = models.DateTimeField("Resolution Time", auto_now_add=True)

    def __str__(self) -> str:
        return f"#{self.ticket.id} resolved by {self.user} at {self.resolved_at}"
