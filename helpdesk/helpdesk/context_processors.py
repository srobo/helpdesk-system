from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

if TYPE_CHECKING:
    from django.http import HttpRequest


def settings_context(request: HttpRequest) -> dict[str, str]:
    return {
        "SYSTEM_TITLE": settings.SYSTEM_TITLE,
    }
