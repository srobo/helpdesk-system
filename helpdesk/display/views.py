from typing import Any

from django.db.models import Q
from django.views.generic import TemplateView

from tickets.models import Ticket, TicketStatus


class HelpdeskDisplayView(TemplateView):

    template_name = "display/helpdesk.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        qs = Ticket.objects.with_event_fields().exclude(Q(status=TicketStatus.RESOLVED) | Q(queue__show_in_overview=False))
        in_progress = qs.filter(assignee_id__isnull=False)
        unassigned = qs.filter(assignee_id__isnull=True)

        return super().get_context_data(
            in_progress=in_progress,
            unassigned=unassigned,
            **kwargs,
        )
