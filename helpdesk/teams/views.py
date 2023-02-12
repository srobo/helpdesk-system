from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from tickets.tables import TicketTable

from .filters import TeamFilterset
from .models import Team
from .tables import TeamTable

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from tickets.models import Ticket


class TeamListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Team
    table_class = TeamTable
    filterset_class = TeamFilterset


class TeamDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    model = Team
    slug_field = "tla"
    table_class = TicketTable

    def get_table_data(self) -> QuerySet[Ticket]:
        return self.object.tickets.all()
