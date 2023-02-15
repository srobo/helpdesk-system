from django.urls import path

from .views import (
    AssignedTicketListView,
    RedirectToDefaultTicketQueue,
    TicketCreateForQueueView,
    TicketDetailView,
    TicketQueueDetailView,
    TicketResolveFormView,
    TicketSubmitCommentFormView,
    TicketUpdateView,
)

app_name = "tickets"

urlpatterns = [
    path("", RedirectToDefaultTicketQueue.as_view(), name="queue_default"),
    path(
        "assigned-to-me", AssignedTicketListView.as_view(), name="ticket_assigned_list",
    ),
    path("<slug:slug>", TicketQueueDetailView.as_view(), name="queue_detail"),
    path("<slug:slug>/new", TicketCreateForQueueView.as_view(), name="queue_create_ticket"),
    path("ticket/<int:pk>", TicketDetailView.as_view(), name="ticket_detail"),
    path("ticket/<int:pk>/edit", TicketUpdateView.as_view(), name="ticket_edit"),
    path("ticket/<int:pk>/comment", TicketSubmitCommentFormView.as_view(), name="ticket_comment"),
    path("ticket/<int:pk>/resolve", TicketResolveFormView.as_view(), name="ticket_resolve"),
]
