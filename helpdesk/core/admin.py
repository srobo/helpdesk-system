from django.contrib import admin

from .models import NavigationLink


class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]


admin.site.register(NavigationLink, NavigationLinkAdmin)
