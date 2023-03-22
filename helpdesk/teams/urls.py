from django.urls import path

from .views import (
    TeamDetailAboutView,
    TeamDetailTicketsView,
    TeamDetailTimelineView,
    TeamListView,
    TicketDetailRedirectView,
)

app_name = "teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="team_list"),
    path("<slug:slug>/", TicketDetailRedirectView.as_view(), name="team_detail"),
    path("<slug:slug>/about", TeamDetailAboutView.as_view(), name="team_detail_about"),
    path("<slug:slug>/tickets", TeamDetailTicketsView.as_view(), name="team_detail_tickets"),
    path("<slug:slug>/timeline", TeamDetailTimelineView.as_view(), name="team_detail_timeline"),
]
