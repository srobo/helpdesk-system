from typing import Any

from django.contrib.admin.utils import NestedObjects
from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from django.db.models import Max

from teams.models import Team, TeamPitLocation
from tickets.models import Ticket

MODELS_TO_TRUNCATE = [Team, Ticket, TeamPitLocation]


class Command(BaseCommand):
    help = "Reset the system for use between years, keeping users"  # noqa: A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--delete", action="store_true", help="Actually delete things")

    def handle(self, **options: Any) -> None:
        collector = NestedObjects(using="default")

        for model in MODELS_TO_TRUNCATE:
            collector.collect(model.objects.all())

        # Ensure items are in cascade deletion order
        collector.sort()

        for model, instances in collector.data.items():
            self.stdout.write(self.style.HTTP_INFO(model._meta.verbose_name_plural.title()))
            for instance in instances:
                self.stdout.write(f"\t- {instance}")

        if not options["delete"]:
            self.stdout.write(self.style.NOTICE("Not deleting anything. Pass --delete to apply"))
            return

        for model, instances in collector.data.items():
            print(model)
            model.objects.filter(pk__in=[i.pk for i in instances]).delete()

        deleted = sum(len(instances) for instances in collector.data.values())
        self.stdout.write(self.style.NOTICE(f"Deleted {deleted} instances."))

        # Reset the primary key counters so they're more pleasing to humans.
        for model in MODELS_TO_TRUNCATE:
            max_id = model.objects.aggregate(Max("id"))["id__max"] or 0
            with connection.cursor() as cursor:
                cursor.execute("UPDATE sqlite_sequence SET seq=? WHERE name=?", [max_id, model._meta.db_table])
