from django.conf import settings


def settings_context(request):
    return {
        "SYSTEM_TITLE": settings.SYSTEM_TITLE,
    }
