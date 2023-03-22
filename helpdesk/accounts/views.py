from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
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

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:profile_update")


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('account_login')
    template_name = 'accounts/signup.html'
