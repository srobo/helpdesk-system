from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


class TeamPitLocation(models.Model):

    name = models.CharField("Name", max_length=100)
    slug = models.CharField("Slug", max_length=30)

    def __str__(self) -> str:
        return self.name


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
    pit_location = models.ForeignKey(TeamPitLocation, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.tla} - {self.name}"

    def get_absolute_url(self) -> str:
        return reverse_lazy('teams:team_detail', kwargs={'tla': self.tla})
