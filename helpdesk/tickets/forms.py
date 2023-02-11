from django import forms


class TicketCommentSubmitForm(forms.Form):

    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
