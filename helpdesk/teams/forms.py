from collections.abc import Mapping
from datetime import datetime
from typing import Any

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from teams.models import Team, TeamAttendanceEvent, TeamBatteryLoan


class TeamAttendanceLogForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = TeamAttendanceEvent
        fields = ("type", "comment", "team")


class TeamBatteryLoanForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.HiddenInput())

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


class DateTimeCheckboxInput(forms.CheckboxInput):
    def format_value(self, value: str) -> str | None:
        if value is True or value is False or value is None or value == "":
            return str(datetime.now(timezone.get_current_timezone()))
        return super().format_value(value)

    def value_from_datadict(
        self, data: Mapping[str, Any | None], files: MultiValueDict[str, UploadedFile], name: str
    ) -> Any | None:
        if name in data:
            return data[name]
        return None


class BooleanDateTimeField(forms.DateTimeField):
    widget = DateTimeCheckboxInput


class TeamBatteryLoanReturnForm(forms.ModelForm):
    battery_1_returned_at = BooleanDateTimeField(label="Battery 1 Returned", required=False)
    battery_2_returned_at = BooleanDateTimeField(label="Battery 2 Returned", required=False)
    charger_returned_at = BooleanDateTimeField(label="Charger Returned", required=False)
    charger_psu_returned_at = BooleanDateTimeField(label="Charger PSU Returned", required=False)
    battery_bag_returned_at = BooleanDateTimeField(label="Battery Bag Returned", required=False)

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
