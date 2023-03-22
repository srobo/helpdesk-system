from __future__ import annotations

from collections.abc import Callable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import resolve


class ProfileMiddleware:

    EXCLUDED_PATHS: set[tuple[str | None, str]] = {
        (None, "account_logout"),
        ("accounts", "profile_update"),
    }

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        profile_complete = getattr(request.user, "first_name", None) and getattr(request.user, "last_name", None)
        if all([
            request.user.is_authenticated,
            not profile_complete,
            self._request_requires_profile(request),
        ]):
            messages.info(request, 'Welcome! Please set up your profile to continue')
            return redirect("accounts:profile_update")
        return self.get_response(request)

    def _request_requires_profile(self, request: HttpRequest) -> bool:
        path_info = resolve(request.path_info)

        if path_info.app_name == "admin":
            return False

        path = (path_info.app_name or None, path_info.url_name)
        return path not in self.EXCLUDED_PATHS
