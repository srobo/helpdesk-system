import django_tables2 as tables

from .models import Team, TeamAttendanceEventType


class TeamTable(tables.Table):
    tla = tables.Column()
    name = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")])
    is_rookie = tables.BooleanColumn()
    actions = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")], text="View")

    class Meta:
        model = Team
        exclude = ("id", "pit_location")
        order_by = "tla"


class TeamAttendanceTable(tables.Table):
    name = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")])
    latest_event__0__type = tables.Column("Latest Event")
    latest_event__0__comment = tables.Column("Comment")
    latest_event__0__created_at = tables.DateTimeColumn(verbose_name="Time")
    user = tables.TemplateColumn(
        verbose_name="Created by",
        template_code='{{record.user|default:"—"}}',
    )
    actions = tables.LinkColumn("teams:team_log_attendance_form", args=[tables.A("tla")], text="Log")

    def render_latest_event__0__type(self, value: str) -> str | None:
        lookups = dict(TeamAttendanceEventType.choices)
        return lookups.get(value)

    class Meta:
        model = Team
        exclude = ["id", "tla", "is_rookie", "pit_location"]
