from django import forms

from teams.models import Team, TeamAttendanceEvent, TeamEvent


class TeamAttendanceLogForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = TeamAttendanceEvent
        fields = ("type", "comment", "team")


class TeamEventForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = TeamEvent
        fields = ("type", "comment", "team")
