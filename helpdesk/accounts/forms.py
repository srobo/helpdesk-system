from hmac import compare_digest

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from accounts.models import User


class SignupForm(UserCreationForm):
    signup_code = forms.CharField(
        label="Volunteer Signup Code",
        help_text="This code verifies that you are a volunteer. It can be found in the break room.",
        widget=forms.PasswordInput(),
        required=True,
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

    def clean_signup_code(self) -> None:
        signup_code = self.cleaned_data.get("signup_code")
        if not compare_digest(signup_code, settings.VOLUNTEER_SIGNUP_CODE):
            raise ValidationError("The Volunteer Signup Code was not correct.")
        return None
