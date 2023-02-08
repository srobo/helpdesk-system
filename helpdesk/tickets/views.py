from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, RedirectView, ListView

from .models import TicketQueue, Ticket


class RedirectToDefaultTicketQueue(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if not (ticket_queue := self.request.user.default_ticket_queue):
            ticket_queue = TicketQueue.objects.first()
        return reverse_lazy('tickets:queue_detail', kwargs={"slug": ticket_queue.slug})

class TicketQueueDetailView(LoginRequiredMixin, DetailView):
    model = TicketQueue

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ticket_queues'] = TicketQueue.objects.all()
        return context


class AssignedTicketListView(LoginRequiredMixin, ListView):
    
    def get_queryset(self):
        return self.request.user.tickets

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ticket_queues'] = TicketQueue.objects.all()
        return context



class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
