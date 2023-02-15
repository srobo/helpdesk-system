from collections.abc import Generator
from typing import Any

from django.contrib import admin

from .models import Ticket, TicketComment, TicketQueue, TicketResolution


class TicketQueueAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class TicketCommentAdmin(admin.StackedInline):
    model = TicketComment
    extra = 1

    readonly_fields = ('created_at', )


class TicketResolutionAdmin(admin.StackedInline):
    model = TicketResolution

    readonly_fields = ('resolved_at', )


class ResolvedFilter(admin.EmptyFieldListFilter):

    def choices(self, changelist: Any) -> Generator[dict[str, Any], None, None]:
        for lookup, title in (
            (None, 'All'),
            ('1', 'Unresolved'),
            ('0', 'Resolved'),
        ):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "queue")
    list_filter = ("queue", ("resolution", ResolvedFilter), "team")

    inlines = (TicketResolutionAdmin, TicketCommentAdmin)

    can_delete = False


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)
