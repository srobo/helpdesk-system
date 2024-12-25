from django.urls import path

from .views import (
    TeamAttendanceFormView,
    TeamAttendanceView,
    TeamDetailAboutView,
    TeamDetailCommentsView,
    TeamDetailTicketsView,
    TeamDetailTimelineView,
    TeamListView,
    TeamSubmitCommentFormView,
    TicketDetailRedirectView,
)

app_name = "teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="team_list"),
    path("attendance", TeamAttendanceView.as_view(), name="team_list_attendance"),
    path("attendance/<slug:tla>", TeamAttendanceFormView.as_view(), name="team_log_attendance_form"),
    path("<slug:slug>/", TicketDetailRedirectView.as_view(), name="team_detail"),
    path("<slug:slug>/about", TeamDetailAboutView.as_view(), name="team_detail_about"),
    path("<slug:slug>/comments", TeamDetailCommentsView.as_view(), name="team_detail_comments"),
    path("<slug:slug>/comments/post", TeamSubmitCommentFormView.as_view(), name="team_detail_comments_post"),
    path("<slug:slug>/tickets", TeamDetailTicketsView.as_view(), name="team_detail_tickets"),
    path("<slug:slug>/timeline", TeamDetailTimelineView.as_view(), name="team_detail_timeline"),
]
