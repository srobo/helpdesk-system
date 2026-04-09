import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Team, TeamAttendanceEvent, TeamAttendanceEventType, TeamBatteryLoan


class TeamTable(tables.Table):
    tla = tables.Column()
    name = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")])
    is_rookie = tables.BooleanColumn()
    actions = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")], text="View")

    class Meta:
        model = Team
        exclude = ("id", "pit_location")
        order_by = "tla"


class TeamAttendanceOverviewTable(tables.Table):
    tla = tables.Column()
    name = tables.LinkColumn("teams:team_detail", args=[tables.A("tla")])
    latest_event__0__type = tables.Column("Latest Event")
    latest_event__0__comment = tables.Column("Comment")
    latest_event__0__created_at = tables.DateTimeColumn(verbose_name="Time", format="D H:i")
    user = tables.TemplateColumn(
        verbose_name="Logged by",
        template_code='{{record.latest_event.0.user|default:"—"}}',
    )
    actions = tables.LinkColumn("teams:team_log_attendance_form", args=[tables.A("tla")], text="Log")

    def render_latest_event__0__type(self, value: str) -> str | None:
        lookups = dict(TeamAttendanceEventType.choices)
        return lookups.get(value)

    class Meta:
        model = Team
        exclude = ["id", "is_rookie", "pit_location"]


class TeamAttendanceListTable(tables.Table):
    type = tables.Column()
    comment = tables.Column()
    created_at = tables.DateTimeColumn(verbose_name="Time", format="D H:i")
    user = tables.TemplateColumn(
        verbose_name="Logged by",
        template_code='{{record.user|default:"—"}}',
    )

    class Meta:
        model = TeamAttendanceEvent
        sequence = ("created_at", "type", "comment", "user")
        order_by = "-created_at"
        exclude = ["id", "team"]


class ReturnedColumn(tables.Column):
    empty_values = ()
    orderable = False
    attrs = {"th": {"class": "is-hidden"}}

    def render(self, value: str | None) -> str:
        if value is not None:
            return format_html('<i class="fa fa-check has-text-success" title="Returned at {date}"></i>', date=value)
        return mark_safe('<i class="fa fa-question has-text-warning" title="Not yet returned"></i>')


class TeamBatteryLoanTable(tables.Table):
    team__tla = tables.Column()
    battery_1_asset_code = tables.Column(verbose_name="Battery 1", attrs={"th": {"colspan": "2"}})
    battery_2_asset_code = tables.Column(verbose_name="Battery 2", attrs={"th": {"colspan": "2"}})
    charger_asset_code = tables.Column(verbose_name="Charger", attrs={"th": {"colspan": "2"}})
    charger_psu_asset_code = tables.Column(verbose_name="Charger PSU", attrs={"th": {"colspan": "2"}})
    battery_bag_asset_code = tables.Column(verbose_name="Battery Bag", attrs={"th": {"colspan": "2"}})
    battery_1_returned_at = ReturnedColumn()
    battery_2_returned_at = ReturnedColumn()
    charger_returned_at = ReturnedColumn()
    charger_psu_returned_at = ReturnedColumn()
    battery_bag_returned_at = ReturnedColumn()
    actions = tables.LinkColumn("teams:team_battery_loan_edit", args=[tables.A("id")], text="Return")

    class Meta:
        model = TeamBatteryLoan
        sequence = (
            "team__tla",
            "battery_1_asset_code",
            "battery_1_returned_at",
            "battery_2_asset_code",
            "battery_2_returned_at",
            "charger_asset_code",
            "charger_returned_at",
            "charger_psu_asset_code",
            "charger_psu_returned_at",
            "battery_bag_asset_code",
            "battery_bag_returned_at",
            "notes",
            "actions",
        )
        exclude = ["id", "team", "user", "created_at"]
