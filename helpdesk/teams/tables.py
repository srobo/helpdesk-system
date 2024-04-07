import django_tables2 as tables

from .models import Team


class TeamTable(tables.Table):
    tla = tables.Column()
    name = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")])
    is_rookie = tables.BooleanColumn()
    actions = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")], text="View")

    class Meta:
        model = Team
        exclude = ("id", "pit_location")
        order_by = "tla"
