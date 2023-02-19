from __future__ import annotations

from typing import Any

import django_filters

from teams.models import Team

from .models import Ticket, TicketQueue


class TicketFilter(django_filters.FilterSet):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.form.initial["resolved"] = False

    resolved = django_filters.BooleanFilter(
        "resolution", "isnull", exclude=True, label="Resolved",
    )
    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(), field_name="queue", to_field_name="slug",
    )
    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(), field_name="team", to_field_name="tla",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []
