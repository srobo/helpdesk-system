from __future__ import annotations

from typing import Any

import django_filters

from accounts.models import User
from teams.models import Team

from .models import Ticket, TicketQueue


class BaseTicketFilter(django_filters.FilterSet):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.form.initial["resolved"] = False

    resolved = django_filters.BooleanFilter(
        "resolution", "isnull", exclude=True, label="Resolved",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []

class AssignedQueueTicketFilter(BaseTicketFilter):
    """Ticket filter for My Tickets page."""

    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(), field_name="team", to_field_name="tla",
    )

    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(), field_name="queue", to_field_name="slug",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []


class QueueTicketFilter(BaseTicketFilter):
    """Ticket filter for a ticket queue."""

    assignee = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), field_name="assignee", to_field_name="username",
    )

    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(), field_name="team", to_field_name="tla",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []


# TODO: TeamTicketFilter for team pages
