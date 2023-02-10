from __future__ import annotations

import django_filters

from .models import Ticket, TicketQueue


class TicketFilter(django_filters.FilterSet):
    resolved = django_filters.BooleanFilter(
        "resolved_at", "isnull", exclude=True, label="Resolved"
    )
    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(), field_name="queue", to_field_name="slug"
    )

    class Meta:
        model = Ticket
        fields: list[str] = []
