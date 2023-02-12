from django_filters import FilterSet, filters

from .models import Team


class TeamFilterset(FilterSet):

    is_rookie = filters.BooleanFilter()

    class Meta:
        model = Team
        fields: list[str] = []
