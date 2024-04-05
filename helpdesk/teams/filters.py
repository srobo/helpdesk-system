from django_filters import FilterSet, filters

from .models import Team, TeamPitLocation


class TeamFilterset(FilterSet):
    is_rookie = filters.BooleanFilter()
    pit_location = filters.ModelChoiceFilter(queryset=TeamPitLocation.objects.all())

    class Meta:
        model = Team
        fields: list[str] = []
