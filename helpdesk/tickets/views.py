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

from helpdesk.forms import CommentSubmitForm
from helpdesk.utils import get_object_or_none
from teams.models import Team

from .filters import TicketFilter
from .forms import TicketAssignForm, TicketCreationForm
from .models import Ticket, TicketEventAssigneeChange, TicketQueue, TicketStatus
from .tables import TicketTable

if TYPE_CHECKING:
    from django import forms
    from django.db.models import QuerySet


class TicketQueueDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    model = TicketQueue
    table_class = TicketTable

    def get_ticket_queryset(self) -> QuerySet[Ticket]:
        queryset = self.get_object().tickets.with_event_fields()
        # Hack: if resolved is not in a query parameter, filter out resolved
        # tickets as a default value.
        if "status" not in self.request.GET:
            queryset = queryset.filter(status=TicketStatus.OPEN)
        return queryset
    
    def get_ticket_filter(self) -> TicketFilter:
        queryset = self.get_ticket_queryset()
        
        return TicketFilter(
            data=self.request.GET or None,
            request=self.request,
            queryset=queryset,
            initial_status=TicketStatus.OPEN,
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
    filterset_class = TicketFilter
    table_class = TicketTable
    template_name = "tickets/ticketqueue_assigned.html"

    def get_queryset(self) -> QuerySet[Ticket]:
        queryset = Ticket.objects.with_event_fields().filter(assignee_id=self.request.user.id)
        # Hack: if resolved is not in a query parameter, filter out resolved
        # tickets as a default value.
        if "status" not in self.request.GET:
            queryset = queryset.filter(status=TicketStatus.OPEN)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context
    

class TicketListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = TicketFilter
    table_class = TicketTable
    template_name = "tickets/tickets_all.html"
    queryset = Ticket.objects.with_event_fields().all()


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket

    def get_queryset(self) -> QuerySet[Ticket]:
        return Ticket.objects.with_event_fields().all()

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        return super().get_context_data(
            comment_form=CommentSubmitForm(),
            assign_form=TicketAssignForm(initial={"user": self.object.assignee}),
            **kwargs,
        )


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreationForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """The same template is used for updating tickets."""
        return super().get_context_data(create=True, **kwargs)
    
    def get_initial(self) -> dict[str, Any]:
        return {
            "team": get_object_or_none(Team, tla=self.request.GET.get("team")),
            "queue": get_object_or_none(TicketQueue, slug=self.request.GET.get("queue")),
        }

    def form_valid(self, form: forms.Form) -> HttpResponse:
        resp =  super().form_valid(form)
        ticket = form.instance # type: ignore[attr-defined]
        ticket.events.create(
            new_status=TicketStatus.OPEN,
            user=self.request.user,
            comment=form.cleaned_data["description"],
        )
        return resp

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ('title', 'queue', 'team')

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
            ticket.queue = ticket.queue.escalation_queue
            ticket.save()
            ticket.events.create(  # TODO: Maybe use an event for escalation?
                assignee_change=TicketEventAssigneeChange.objects.get_or_create(user=None)[0],
                comment=f"Escalated to {ticket.queue}",
                user=self.request.user,
            )
            return HttpResponseRedirect(redirect_to=self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form: Form) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TicketAssignToUserFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Ticket
    form_class = TicketAssignForm

    def get_queryset(self) -> QuerySet[Ticket]:
        return Ticket.objects.with_event_fields().all()

    def get_success_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={"pk": self.get_object().id})

    def form_valid(self, form: Form) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket: Ticket = self.get_object()
        new_assignee = form.cleaned_data["user"]

        if ticket.assignee != new_assignee:
            # Only post a change if the user changed.
            assignee_change, _ = TicketEventAssigneeChange.objects.get_or_create(user=new_assignee)
            ticket.events.create(
                assignee_change=assignee_change,
                comment=form.cleaned_data.get("comment", None),
                user=self.request.user,
            )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def form_invalid(self, form: Form) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TicketSubmitCommentFormView(LoginRequiredMixin, FormMixin, SingleObjectMixin, ProcessFormView):

    http_method_names = ['post', 'put']
    model = Ticket
    form_class = CommentSubmitForm
    new_status = ""

    def get_success_url(self) -> str:
        return reverse_lazy('tickets:ticket_detail', kwargs={"pk": self.get_object().id})

    def form_valid(self, form: CommentSubmitForm) -> HttpResponse:
        assert self.request.user.is_authenticated
        ticket = self.get_object()
        ticket.events.create(
            new_status=self.new_status,
            comment=form.cleaned_data['comment'],
            user=self.request.user,
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def form_invalid(self, form: CommentSubmitForm) -> HttpResponse:
        return HttpResponse("Please fill out the form correctly.")


class TicketResolveFormView(TicketSubmitCommentFormView):

    new_status = TicketStatus.RESOLVED


class TicketReOpenFormView(TicketSubmitCommentFormView):

    new_status = TicketStatus.OPEN
