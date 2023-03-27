from django import forms

from accounts.models import User

from .models import Ticket


class TicketCreationForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))

    class Meta:
        model = Ticket
        fields = ('title', 'queue', 'team')


class TicketAssignForm(forms.Form):

    user = forms.ModelChoiceField(User.objects.all(), to_field_name="username", required=False)
    comment = forms.CharField(label="Optional Comment", widget=forms.Textarea(attrs={"rows": "3"}), required=False)
