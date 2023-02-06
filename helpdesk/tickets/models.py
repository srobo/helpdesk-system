from django.db import models

class TicketQueue(models.Model):

    name = models.CharField("Ticket Queue Name", max_length=32)
    slug = models.SlugField("Slug", max_length=32)

    def __str__(self) -> str:
        return f"Ticket Queue: {self.name}"

class TicketStatus(models.TextChoices):

    OPEN = ("OP", "Open")
    AWAITING_RESPONSE = ("AR", "Awaiting Team Response")
    BLOCKED = ("BL", "Blocked")
    CLOSED = ("CL", "Closed")


class TicketPriority(models.TextChoices):

    LOW = ("L", "Low")
    NORMAL = ("N", "Normal")
    HIGH = ("H", "High")


class Ticket(models.Model):

    title = models.CharField(max_length=120)
    queue = models.ForeignKey(TicketQueue, on_delete=models.PROTECT, related_name="tickets", related_query_name="tickets")

    status = models.CharField(max_length=2, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    priority = models.CharField(max_length=1, choices=TicketPriority.choices, default=TicketPriority.NORMAL)

    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name="tickets", related_query_name="tickets")

    opened_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name=None, related_query_name=None)
    assignee = models.ForeignKey('accounts.User', on_delete=models.PROTECT, null=True, blank=True, related_name="tickets", related_query_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"#{self.id} - {self.title}"
