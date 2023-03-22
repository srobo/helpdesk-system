from __future__ import annotations

from collections.abc import Generator
from typing import Any, Literal, TypedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django_tables2 import SingleTableMixin

from helpdesk.tables import SearchTable
from teams.models import Team
from tickets.models import Ticket


class RedirectToDefaultTicketQueue(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *arg: Any, **kwargs: Any) -> str | None:
        assert self.request.user.is_authenticated

        # Redirect the user to a default queue if they have one
        if ticket_queue := self.request.user.default_ticket_queue:
            return reverse_lazy(
                "tickets:queue_detail", kwargs={"slug": ticket_queue.slug},
            )
        else:
            return reverse_lazy("teams:team_list")


class SearchResult(TypedDict):

    result_type: Literal["team"] | Literal["ticket"]
    title: str
    url: str


class SearchView(LoginRequiredMixin, SingleTableMixin, TemplateView):
    
    template_name = "search.html"
    table_class = SearchTable

    def _get_query(self) -> str:
        return self.request.GET.get("q", "")

    def _get_filters(self, q: str) -> dict[type[Ticket] | type[Team], Q]:
        return {
            Ticket: Q(title__icontains=q, comments__content__icontains=q),
            Team: Q(tla__icontains=q) | Q(name__icontains=q),
        }
    
    def get_result_count(self, q: str) -> int:
        filters = self._get_filters(q)
        return sum(
            [
                model.objects.filter(q_filter).count()
                for model, q_filter in filters.items()
            ],
        )

    def get_results(self, q: str) -> Generator[SearchResult, None, None]:
        filters = self._get_filters(q)

        for team in Team.objects.filter(filters[Team]):
            yield SearchResult(result_type='team', title=team.name, url=team.get_absolute_url())

        for ticket in Ticket.objects.filter(filters[Ticket]):
            yield SearchResult(result_type='ticket', title=ticket.title, url=ticket.get_absolute_url())

    def get_table_data(self) -> Generator[SearchResult, None, None]:
        q = self._get_query()
        return self.get_results(q)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        q = self._get_query()

        result_count = self.get_result_count(q)
        if result_count == 1:
            result = list(self.get_results(q))[0]
            return HttpResponseRedirect(redirect_to=result["url"])

        context = self.get_context_data(q=q)
        return self.render_to_response(context)
