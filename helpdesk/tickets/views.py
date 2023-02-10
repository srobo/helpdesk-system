from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, RedirectView
from django_filters.views import FilterView

from .filters import TicketFilter
from .models import Ticket, TicketQueue

if TYPE_CHECKING:
    from django.db.models import QuerySet


class RedirectToDefaultTicketQueue(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *arg: Any, **kwargs: Any) -> str | None:
        assert self.request.user.is_authenticated
        if not (ticket_queue := self.request.user.default_ticket_queue):
            ticket_queue = TicketQueue.objects.first()

        # ticket_queue can be None if no queues exist.
        if ticket_queue:
            return reverse_lazy(
                "tickets:queue_detail", kwargs={"slug": ticket_queue.slug}
            )
        else:
            return reverse_lazy("tickets:ticket_assigned_list")


class TicketQueueDetailView(LoginRequiredMixin, DetailView):
    model = TicketQueue

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context


class AssignedTicketListView(LoginRequiredMixin, FilterView):
    filterset_class = TicketFilter

    def get_queryset(self) -> QuerySet[Ticket]:
        assert self.request.user.is_authenticated
        return self.request.user.tickets.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
