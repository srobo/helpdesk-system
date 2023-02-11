from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_tables2 import SingleTableView

from .models import Team
from .tables import TeamTable


class TeamListView(LoginRequiredMixin, SingleTableView):
    model = Team
    table_class = TeamTable


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    slug_field = "tla"
