from django.contrib import admin

from teams.models import Team, TeamPitLocation


class TeamPitLocationAdmin(admin.ModelAdmin):
    list_display = ("name", )


class TeamAdmin(admin.ModelAdmin):
    list_display = ("tla", "name", "is_rookie")
    list_filter = ("is_rookie",)


admin.site.register(TeamPitLocation, TeamPitLocationAdmin)
admin.site.register(Team, TeamAdmin)
