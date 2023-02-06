from django.contrib import admin

from .models import Ticket, TicketQueue


class TicketQueueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class TicketAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)
