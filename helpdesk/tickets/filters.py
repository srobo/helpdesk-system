from __future__ import annotations

import django_filters
from teams.models import Team

from .models import Ticket, TicketQueue


class TicketFilter(django_filters.FilterSet):
    resolved = django_filters.BooleanFilter(
        "resolution", "isnull", exclude=True, label="Resolved"
    )
    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(), field_name="queue", to_field_name="slug"
    )
    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(), field_name="team", to_field_name="tla",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []
