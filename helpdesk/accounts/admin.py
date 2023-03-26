from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Competition"), {"fields": ("default_ticket_queue",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "onboarded_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "password1", "password2"),
            },
        ),
        (
            "Competition",
            {
                "classes": ("wide",),
                "fields": ("default_ticket_queue",),
            },
        ),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "default_ticket_queue",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "default_ticket_queue",
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    search_fields = ("username", "first_name", "last_name", "email")


admin.site.register(User, CustomUserAdmin)
