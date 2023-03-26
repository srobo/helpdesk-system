import django_tables2 as tables

from .models import Ticket, TicketStatus


class TicketTable(tables.Table):

    id = tables.TemplateColumn("<strong>#{{record.id}}</strong>")  # noqa: A003
    title = tables.LinkColumn('tickets:ticket_detail', args=[tables.A('id')])
    team = tables.LinkColumn(
        'teams:team_detail',
        args=[tables.A('team.tla')],
        accessor=tables.A('team.tla'),
        verbose_name="Team",
    )
    status = tables.Column()
    assignee = tables.Column()
    actions = tables.LinkColumn('tickets:ticket_detail', args=[tables.A('id')], text="View")

    class Meta:
        model = Ticket
        fields: list[str] = []
        order_by = 'created_at'

    def render_status(self, value: str) -> str:
        lookups = {val: name for val, name in TicketStatus.choices}
        return lookups.get(value, "Unknown")
