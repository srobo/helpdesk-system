from __future__ import annotations

from typing import Any

import django_filters

from teams.models import Team, TeamPitLocation

from .models import Ticket, TicketQueue, TicketStatus


class TicketFilter(django_filters.FilterSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        initial_status = kwargs.pop("initial_status", None)
        super().__init__(*args, **kwargs)
        if initial_status is not None:
            self.form.initial["status"] = initial_status

    status = django_filters.ChoiceFilter(label="Status", choices=TicketStatus.choices)
    # assignee_id = django_filters.ChoiceFilter(
    #     label="Assignee",
    #     choices=[(user.id, user.get_full_name()) for user in User.objects.all()],
    # )
    queue = django_filters.ModelChoiceFilter(
        queryset=TicketQueue.objects.all(),
        field_name="queue",
        to_field_name="slug",
    )
    team = django_filters.ModelChoiceFilter(
        queryset=Team.objects.all(),
        field_name="team",
        to_field_name="tla",
    )
    team__pit_location = django_filters.ModelChoiceFilter(
        label="Pit location",
        queryset=TeamPitLocation.objects.all(),
    )

    class Meta:
        model = Ticket
        fields: list[str] = []
