import django_tables2 as tables

from .models import Ticket


class TicketTable(tables.Table):

    id = tables.TemplateColumn("<strong>#{{record.id}}</strong>")  # noqa: A003
    title = tables.LinkColumn('tickets:ticket_detail', args=[tables.A('id')])
    team = tables.LinkColumn(
        'teams:team_detail',
        args=[tables.A('team.tla')],
        accessor=tables.A('team.tla'),
        verbose_name="Team",
    )
    assignee = tables.Column()
    resolution = tables.TemplateColumn(
        "{% if record.resolution %}Resolved{% else %}Open{% endif %}",
        verbose_name="Status",
    )
    actions = tables.LinkColumn('tickets:ticket_detail', args=[tables.A('id')], text="View")

    class Meta:
        model = Ticket
        fields: list[str] = []
        order_by = 'created_at'
