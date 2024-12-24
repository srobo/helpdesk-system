from django import forms

from teams.models import Team, TeamAttendanceEvent, TeamAttendanceEventType


class TeamAttendanceLogForm(forms.ModelForm):
    type = forms.Select(choices=TeamAttendanceEventType.choices)
    comment = forms.CharField(required=False)

    class Meta:
        model = TeamAttendanceEvent
        fields = ("type", "comment", "team")
