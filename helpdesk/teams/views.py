from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .filters import TeamFilterset
from .models import Team
from .tables import TeamTable


class TeamListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Team
    table_class = TeamTable
    filterset_class = TeamFilterset


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    slug_field = "tla"
