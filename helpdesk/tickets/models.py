from django.db import models
from django.utils import timezone


class TicketQueue(models.Model):
    name = models.CharField("Ticket Queue Name", max_length=32)
    slug = models.SlugField("Slug", max_length=32)

    def __str__(self) -> str:
        return f"Ticket Queue: {self.name}"
    
    def active_tickets(self):
        return self.tickets.filter(resolved_at__isnull=True)


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
    resolved_at = models.DateTimeField("Resolved Time", null=True, blank=True)
    resolved_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, null=True, related_name="resolved_tickets", related_query_name="resolved_tickets")

    class Meta:
        ordering = ['created_at']


    def __str__(self) -> str:
        return f"#{self.id} - {self.title}"
    
    def mark_resolved(self, user) -> None:
        self.resolved_at = timezone.now()
        self.resolved_by = user
        self.save()


class TicketComment(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments", related_query_name="comments")
    content = models.TextField()
    author = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name="comments", related_query_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"Comment on #{self.ticket.id} at {self.created_at} by {self.author}"