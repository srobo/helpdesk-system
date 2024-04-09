from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django import template
from django.forms import Field
from django_filters.fields import ChoiceField

if TYPE_CHECKING:
    from django_filters import FilterSet

register = template.Library()


def _get_value_display_for_choices(choice_field: ChoiceField, value: Any) -> Any:
    choices = dict(choice_field.choices.choices)
    return choices.get(value, value)


def _get_value_display_for_field(field: Field, value: Any) -> Any:
    if isinstance(field, ChoiceField):
        return _get_value_display_for_choices(field, value)

    return value


@register.inclusion_tag("inc/tags/filter_badges.html")
def render_filter_badges(filterset: FilterSet) -> dict[str, Any]:
    if filterset.is_valid():  # type: ignore[no-untyped-call]
        cleaned_data = {k: v for k, v in filterset.form.cleaned_data.items() if v is not None and v != ""}
    else:
        cleaned_data = {}

    filter_badges = {
        (
            filterset.form.fields[field_name].label,
            _get_value_display_for_field(filterset.form.fields[field_name], value),
        )
        for field_name, value in cleaned_data.items()
    }

    return {"filter_badges": filter_badges}
