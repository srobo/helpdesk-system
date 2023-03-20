from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormMixin, ProcessFormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from accounts.models import User
from helpdesk.utils import get_object_or_none
from teams.models import Team

from .filters import AssignedQueueTicketFilter, QueueTicketFilter, TicketFilter
from .forms import TicketCommentSubmitForm
from .models import Ticket, TicketQueue, TicketResolution
from .tables import TicketTable

if TYPE_CHECKING:
    from django import forms
    from django.db.models import QuerySet


class TicketQueueDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    model = TicketQueue
    table_class = TicketTable

    def get_ticket_queryset(self) -> QuerySet[Ticket]:
        queryset = self.get_object().tickets.all()
        # Hack: if resolved is not in a query parameter, filter out resolved
        # tickets as a default value.
        if "resolved" not in self.request.GET:
            queryset = queryset.filter(resolution__isnull=True)
        return queryset
    
    def get_ticket_filter(self) -> QueueTicketFilter:
        queryset = self.get_ticket_queryset()
        
        return QueueTicketFilter(
            data=self.request.GET or None,
            request=self.request,
            queryset=queryset,
        )

    def get_table_data(self) -> QuerySet[Ticket]:
        data_filter = self.get_ticket_filter()
        return data_filter.qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        context["filter"] = self.get_ticket_filter()
        return context


class AssignedTicketListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = AssignedQueueTicketFilter
    table_class = TicketTable
    template_name = "tickets/ticketqueue_assigned.html"

    def get_queryset(self) -> QuerySet[Ticket]:
        assert self.request.user.is_authenticated
        queryset = self.request.user.tickets.all()

        # Hack: if resolved is not in a query parameter, filter out resolved
        # tickets as a default value.
        if "resolved" not in self.request.GET:
            queryset = queryset.filter(resolution__isnull=True)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context
    

class TicketListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = TicketFilter
    table_class = TicketTable
    template_name = "tickets/tickets_all.html"
    queryset = Ticket.objects.all()


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        return super().get_context_data(
            comment_form=TicketCommentSubmitForm(),
            **kwargs,
        )


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ('title', 'assignee', 'queue', 'team', 'description')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """The same template is used for updating tickets."""
        return super().get_context_data(create=True, **kwargs)
    
    def get_initial(self) -> dict[str, Any]:
        return {
            "assignee": get_object_or_none(User, username=self.request.GET.get("assignee")),
            "team": get_object_or_none(Team, tla=self.request.GET.get("team")),
            "queue": get_object_or_none(TicketQueue, slug=self.request.GET.get("queue")),
        }

    def form_valid(self, form: forms.Form) -> HttpResponse:
        form.instance.opened_by = self.request.user  # type: ignore[attr-defined]
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ('title', 'assignee', 'queue', 'team', 'description')

class TicketEscalateFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Ticket
    form_class = Form

    def get_success_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={"pk": self.get_object().id})

    def form_valid(self, form: Form) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket: Ticket = self.get_object()
        if ticket.queue.escalation_queue:
            ticket.assignee = None
            ticket.queue = ticket.queue.escalation_queue
            ticket.save()
            ticket.comments.create(
                content=f"Escalated to {ticket.queue}",
                author=self.request.user,
            )
            return HttpResponseRedirect(redirect_to=self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form: Form) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")

class TicketAssignToCurrentUserFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Ticket
    form_class = Form

    def get_success_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={"pk": self.get_object().id})

    def form_valid(self, form: Form) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket: Ticket = self.get_object()
        ticket.assignee = self.request.user
        ticket.save(update_fields=["assignee"])
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def form_invalid(self, form: Form) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TicketSubmitCommentFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Ticket
    form_class = TicketCommentSubmitForm

    def get_success_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={"pk": self.get_object().id})

    def form_valid(self, form: TicketCommentSubmitForm) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket = self.get_object()
        ticket.comments.create(
            content=form.cleaned_data['comment'],
            author=self.request.user,
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def form_invalid(self, form: TicketCommentSubmitForm) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TicketResolveFormView(TicketSubmitCommentFormView):

    def form_valid(self, form: TicketCommentSubmitForm) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket = self.get_object()
        TicketResolution.objects.create(
            ticket=ticket,
            user=self.request.user,
            comment=form.cleaned_data['comment'],
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())
