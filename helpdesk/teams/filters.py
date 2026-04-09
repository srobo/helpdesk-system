from django.db.models import Q, QuerySet
from django_filters import FilterSet, filters

from .models import Team, TeamBatteryLoan, TeamPitLocation


class TeamFilterset(FilterSet):
    is_rookie = filters.BooleanFilter()
    pit_location = filters.ModelChoiceFilter(queryset=TeamPitLocation.objects.all())

    class Meta:
        model = Team
        fields: list[str] = []


class TeamBatteryLoanFilter(FilterSet):
    STATE_CHOICES = (
        ("IC", "Incomplete"),
        ("OC", "Only complete"),
        ("AL", "All"),
    )

    state = filters.TypedChoiceFilter(label="State", method="filter_state", choices=STATE_CHOICES)

    def filter_state(self, queryset: QuerySet[TeamBatteryLoan], _: str, value: str) -> QuerySet[TeamBatteryLoan]:
        if value == "OC":
            return queryset.filter(
                Q(battery_1_returned_at__isnull=False)
                & Q(battery_2_returned_at__isnull=False)
                & Q(charger_returned_at__isnull=False)
                & Q(charger_psu_returned_at__isnull=False)
                & Q(battery_bag_returned_at__isnull=False)
            )
        elif value == "AL":
            return queryset.filter(
                Q(battery_1_returned_at__isnull=True)
                | Q(battery_2_returned_at__isnull=True)
                | Q(charger_returned_at__isnull=True)
                | Q(charger_psu_returned_at__isnull=True)
                | Q(battery_bag_returned_at__isnull=True)
            )
        return queryset

    class Meta:
        model = TeamBatteryLoan
        fields: list[str] = ["state"]
