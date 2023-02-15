from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormMixin, ProcessFormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from teams.models import Team

from .filters import TicketFilter
from .forms import TicketCommentSubmitForm
from .models import Ticket, TicketQueue, TicketResolution
from .tables import TicketTable

if TYPE_CHECKING:
    from django import forms
    from django.db.models import QuerySet


class RedirectToDefaultTicketQueue(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *arg: Any, **kwargs: Any) -> str | None:
        assert self.request.user.is_authenticated
        if not (ticket_queue := self.request.user.default_ticket_queue):
            ticket_queue = TicketQueue.objects.first()

        # ticket_queue can be None if no queues exist.
        if ticket_queue:
            return reverse_lazy(
                "tickets:queue_detail", kwargs={"slug": ticket_queue.slug},
            )
        else:
            return reverse_lazy("tickets:ticket_assigned_list")


class TicketQueueDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    model = TicketQueue
    table_class = TicketTable

    def get_table_data(self) -> QuerySet[Ticket]:
        return self.get_object().tickets.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context


class AssignedTicketListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    filterset_class = TicketFilter
    table_class = TicketTable

    def get_queryset(self) -> QuerySet[Ticket]:
        assert self.request.user.is_authenticated
        return self.request.user.tickets.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_queues"] = TicketQueue.objects.all()
        return context


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

    def form_valid(self, form: forms.Form) -> HttpResponse:
        form.instance.opened_by = self.request.user  # type: ignore[attr-defined]
        return super().form_valid(form)


class TicketCreateForQueueView(TicketCreateView):
    def get_initial(self) -> dict[str, Any]:
        try:
            return {
                "queue": TicketQueue.objects.get(slug=self.kwargs["slug"]),
            }
        except KeyError:
            return {}
        except TicketQueue.DoesNotExist:
            raise Http404("No such queue") from None


class TicketCreateForTeamView(TicketCreateView):
    def get_initial(self) -> dict[str, Any]:
        try:
            return {
                "team": Team.objects.get(tla=self.kwargs["slug"]),
            }
        except KeyError:
            return {}
        except Team.DoesNotExist:
            raise Http404("No such team") from None


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ('title', 'assignee', 'queue', 'team', 'description')


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
