from django.contrib import admin

from .models import Ticket, TicketEvent, TicketEventAssigneeChange, TicketQueue


class TicketQueueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_priority")


class TicketEventAdmin(admin.StackedInline):
    model = TicketEvent
    extra = 1

    readonly_fields = ("created_at",)


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "queue")
    list_filter = ("queue", "team")

    inlines = (TicketEventAdmin,)

    can_delete = False


class TicketEventAssigneeChangeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)
admin.site.register(TicketEventAssigneeChange, TicketEventAssigneeChangeAdmin)
