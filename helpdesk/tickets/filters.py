from __future__ import annotations

import django_filters

from accounts.models import User
from teams.models import Team

from .models import Ticket, TicketQueue, TicketStatus


class BaseTicketFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(label="Status", choices=TicketStatus.choices)

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


class TeamTicketFilter(BaseTicketFilter):
    """Ticket filter for a team page."""

    assignee = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), field_name="assignee", to_field_name="username",
    )

    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(), field_name="queue", to_field_name="slug",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []


class TicketFilter(TeamTicketFilter):
    """Ticket filter for all tickets."""

    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(), field_name="team", to_field_name="tla",
    )

    class Meta:
        model = Ticket
        fields: list[str] = []
