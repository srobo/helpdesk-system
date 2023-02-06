from django.core.validators import RegexValidator
from django.db import models


class Team(models.Model):
    tla = models.CharField(
        "TLA",
        max_length=3,
        unique=True,
        validators=[
            RegexValidator(r"^[A-Z]{3}\d*$", "Must match TLA format."),
        ],
    )
    name = models.CharField("Team Name", max_length=100)
    is_rookie = models.BooleanField("Is Rookie")

    def __str__(self) -> str:
        return f"{self.tla} - {self.name}"
