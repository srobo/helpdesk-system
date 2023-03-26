from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
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
        # Modify generated form to require a name.
        form.fields['first_name'].required = True
        form.fields['first_name'].label = "Given name"
        return form

    def get_success_url(self) -> str:
        messages.success(self.request, "Profile updated.")
        return reverse_lazy("accounts:profile_update")


class OnboardingView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "default_ticket_queue"]
    template_name = "accounts/onboarding.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        assert self.request.user.is_authenticated
        if self.request.user.onboarded_at:
            messages.warning(self.request, "Unable to onboard twice.")
            return HttpResponseRedirect(redirect_to=reverse_lazy("home"))
        return super().dispatch(request, *args, **kwargs)  # type: ignore[return-value]

    def get_object(self, queryset: models.QuerySet[User] | None = None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        # Modify generated form to require a name.
        form.fields['first_name'].required = True
        form.fields['first_name'].label = "Given name"
        return form
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.info(self.request, f"Welcome to {settings.SYSTEM_TITLE}!")
        self.object.onboarded_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("home")


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('account_login')
    template_name = 'accounts/signup.html'
