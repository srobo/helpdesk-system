import django_tables2 as tables

from .models import Ticket, TicketStatus


class TicketTable(tables.Table):
    id = tables.TemplateColumn("<strong>#{{record.id}}</strong>")  # noqa: A003
    title = tables.LinkColumn("tickets:ticket_detail", args=[tables.A("id")])
    team = tables.LinkColumn(
        "teams:team_detail",
        args=[tables.A("team__tla")],
        accessor=tables.A("team__tla"),
        verbose_name="Team",
    )
    status = tables.Column()
    assignee_id = tables.TemplateColumn(
        verbose_name="Assignee",
        template_code='{{record.assignee|default:"—"}}',
    )
    actions = tables.LinkColumn("tickets:ticket_detail", args=[tables.A("id")], text="View")

    class Meta:
        model = Ticket
        fields: list[str] = []
        order_by = "created_at"

    def render_status(self, value: str) -> str:
        lookups = dict(TicketStatus.choices)
        return lookups.get(value, "Unknown")
