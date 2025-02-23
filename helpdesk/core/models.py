from django.db import models


class NavigationLink(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
