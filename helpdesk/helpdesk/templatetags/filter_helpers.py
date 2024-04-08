from typing import Any

from django import template
from django.forms import Field
from django_filters.fields import ChoiceField

register = template.Library()


def _get_value_display_for_choices(choice_field: ChoiceField, value: Any) -> Any:
    choices = dict(choice_field.choices.choices)
    return choices.get(value, value)


def _get_value_display_for_field(field: Field, value: Any) -> Any:
    if isinstance(field, ChoiceField):
        return _get_value_display_for_choices(field, value)

    return value


@register.inclusion_tag("inc/tags/filter_badges.html", takes_context=True)
def render_filter_badges(context: dict[str, Any]) -> dict[str, Any]:
    fltr = context["filter"]

    if fltr.is_valid():
        cleaned_data = {k: v for k, v in fltr.form.cleaned_data.items() if v is not None and v != ""}
    else:
        cleaned_data = {}

    filter_badges = {
        (fltr.form.fields[field_name].label, _get_value_display_for_field(fltr.form.fields[field_name], value))
        for field_name, value in cleaned_data.items()
    }

    return {"filter_badges": filter_badges}
