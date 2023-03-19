from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    # Helpdesk Specific Fields
    default_ticket_queue = models.ForeignKey(
        "tickets.TicketQueue",
        null=True,
        on_delete=models.PROTECT,
        related_query_name=None,
        related_name=None,
        verbose_name="Default Ticket Queue",
    )

    def __str__(self) -> str:
        return self.get_full_name() or self.get_short_name() or self.get_username()
