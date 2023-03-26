from django.contrib import admin

from .models import Ticket, TicketEvent, TicketQueue


class TicketQueueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_priority")


class TicketEventAdmin(admin.StackedInline):
    model = TicketEvent
    extra = 1

    readonly_fields = ('created_at', )


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "queue")
    list_filter = ("queue", "team")

    inlines = (TicketEventAdmin, )

    can_delete = False


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)
