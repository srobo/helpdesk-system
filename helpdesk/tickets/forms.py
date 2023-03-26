from django import forms

from .models import Ticket


class TicketCreationForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))

    class Meta:
        model = Ticket
        fields = ('title', 'assignee', 'queue', 'team')
