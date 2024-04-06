from django import forms


class CommentSubmitForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
