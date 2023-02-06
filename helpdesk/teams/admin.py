from django.contrib import admin
from teams.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ("tla", "name", "is_rookie")
    list_filter = ("is_rookie",)


admin.site.register(Team, TeamAdmin)
