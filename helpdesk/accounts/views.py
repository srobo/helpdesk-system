from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.forms import BaseModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm
from .models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "default_ticket_queue"]

    def get_object(self, queryset: models.QuerySet[User] | None = None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user
    
    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        # Modify generated form to require name fields.
        form.fields["first_name"].required = True
        form.fields["last_name"].required = True
        return form

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:profile_update")


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('account_login')
    template_name = 'accounts/signup.html'
