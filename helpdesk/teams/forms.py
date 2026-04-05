from typing import Any

from django import forms
from django.forms import BooleanField
from django.utils import timezone

from teams.models import Team, TeamAttendanceEvent, TeamBatteryLoan


class TeamAttendanceLogForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = TeamAttendanceEvent
        fields = ("type", "comment", "team")


class TeamBatteryLoanForm(forms.ModelForm):
    class Meta:
        model = TeamBatteryLoan
        fields = (
            "battery_1_asset_code",
            "battery_2_asset_code",
            "charger_asset_code",
            "charger_psu_asset_code",
            "battery_bag_asset_code",
            "notes",
        )


class TeamBatteryLoanReturnForm(forms.ModelForm):
    battery_1_returned_at = BooleanField(label="Battery 1 Returned", required=False)
    battery_2_returned_at = BooleanField(label="Battery 2 Returned", required=False)
    charger_returned_at = BooleanField(label="Charger Returned", required=False)
    charger_psu_returned_at = BooleanField(label="Charger PSU Returned", required=False)
    battery_bag_returned_at = BooleanField(label="Battery Bag Returned", required=False)

    def clean(self) -> dict[str, Any] | None:
        for field in self.fields:
            if field.endswith("_returned_at") and self.cleaned_data.get(field):
                existing_value = getattr(self.instance, field)
                form_value = self.cleaned_data[field]
                if existing_value is None and form_value:
                    self.cleaned_data[field] = timezone.now()
        return super().clean()

    class Meta:
        model = TeamBatteryLoan
        fields = (
            "battery_1_returned_at",
            "battery_2_returned_at",
            "charger_returned_at",
            "charger_psu_returned_at",
            "battery_bag_returned_at",
            "notes",
        )
