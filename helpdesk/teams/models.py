from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.validators import RegexValidator
from django.db import models

if TYPE_CHECKING:
    from tickets.models import Ticket


class Team(models.Model):
    tla = models.CharField(
        "TLA",
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(r"^[A-Z]{3}\d*$", "Must match TLA format."),
        ],
    )
    name = models.CharField("Team Name", max_length=100)
    is_rookie = models.BooleanField("Is Rookie")

    def __str__(self) -> str:
        return f"{self.tla} - {self.name}"

    def active_tickets(self) -> models.QuerySet[Ticket]:
        return self.tickets.filter(resolved_at__isnull=True)
