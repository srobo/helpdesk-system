from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Team


class TeamListView(LoginRequiredMixin, ListView):
    model = Team


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    slug_field = 'tla'
