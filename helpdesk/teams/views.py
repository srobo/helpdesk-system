from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from tickets.filters import TeamTicketFilter
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

    def get_ticket_queryset(self) -> QuerySet[Ticket]:
        return self.get_object().tickets.all()
    
    def get_ticket_filter(self) -> TeamTicketFilter:
        queryset = self.get_ticket_queryset()
        
        return TeamTicketFilter(
            data=self.request.GET or None,
            request=self.request,
            queryset=queryset,
            initial_resolution=None,
        )

    def get_table_data(self) -> QuerySet[Ticket]:
        data_filter = self.get_ticket_filter()
        return data_filter.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filter"] = self.get_ticket_filter()
        return context
