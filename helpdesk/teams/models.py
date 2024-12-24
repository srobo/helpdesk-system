from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


class TeamPitLocation(models.Model):
    name = models.CharField("Name", max_length=100)
    slug = models.CharField("Slug", max_length=30, unique=True)

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

    class Meta:
        ordering = ["tla"]

    def __str__(self) -> str:
        return f"{self.tla} - {self.name}"

    def get_absolute_url(self) -> str:
        return reverse_lazy("teams:team_detail", args=[self.tla])


class TeamComment(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comments",
    )
    content = models.TextField()
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="team_comments",
        related_query_name="team_comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment on {self.team.name} at {self.created_at} by {self.author}"


class TeamAttendanceEventType(models.TextChoices):
    ARRIVED = "AR", "Arrived"
    LEFT = "LE", "Left"
    DELAYED = "DE", "Delayed"
    DROPPED_OUT = "DO", "Dropped Out"


class TeamAttendanceEvent(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_attendance_events",
        related_query_name="team_attendance_events",
    )
    type = models.TextField(
        max_length=2,
        choices=TeamAttendanceEventType.choices,
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
