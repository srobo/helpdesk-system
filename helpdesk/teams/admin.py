from django.contrib import admin

from teams.models import Team, TeamComment, TeamEvent, TeamPitLocation


class TeamPitLocationAdmin(admin.ModelAdmin):
    list_display = ("name",)


class TeamCommentAdmin(admin.StackedInline):
    model = TeamComment
    extra = 1

    readonly_fields = ("created_at",)


class TeamEventAdmin(admin.StackedInline):
    model = TeamEvent
    extra = 1

    readonly_fields = ("created_at",)


class TeamAdmin(admin.ModelAdmin):
    list_display = ("tla", "name", "is_rookie")
    list_filter = ("is_rookie",)
    inlines = (TeamCommentAdmin, TeamEventAdmin)


admin.site.register(TeamPitLocation, TeamPitLocationAdmin)
admin.site.register(Team, TeamAdmin)
