from django.contrib import admin

from .models import Ticket, TicketComment, TicketQueue


class TicketQueueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class TicketCommentAdmin(admin.StackedInline):
    model = TicketComment
    extra = 1


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "queue", "resolved_at")
    list_filter = ("queue", "resolved_at", "team")

    inlines = (TicketCommentAdmin,)

    can_delete = False


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)
