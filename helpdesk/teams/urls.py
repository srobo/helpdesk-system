from django.urls import path

from .views import TeamDetailView, TeamListView

app_name = "teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="team_list"),
    path("<slug:slug>", TeamDetailView.as_view(), name="team_detail"),
]
