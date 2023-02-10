import csv
import datetime
import random
from pathlib import Path

import freezegun
from accounts.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker
from teams.models import Team
from tickets.models import Ticket, TicketQueue

COMP_DAYS = [datetime.date(2023, 4, 1), datetime.date(2023, 4, 2)]
COMP_OPEN_TIME = datetime.time(9)
COMP_CLOSE_TIME = datetime.time(17)


class Command(BaseCommand):
    help = "Generate demo data."  # noqa: A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("teams_data", type=Path)

    def _generate_teams(self, teams_data: Path) -> list[Team]:
        Team.objects.all().delete()
        with teams_data.resolve().open("r") as fh:
            return [
                Team.objects.create(
                    tla=row["TLA"],
                    name=row["School / Institution Name"],
                    is_rookie=row["Competed Before"].startswith("No"),
                )
                for row in csv.DictReader(fh)
                if row["TLA"]
            ]

    def _generate_queues(self) -> list[TicketQueue]:
        queues = []
        queues.append(TicketQueue.objects.create(name="Helpdesk", slug="helpdesk"))
        queues.append(TicketQueue.objects.create(name="Kit Experts", slug="experts"))
        return queues

    def _generate_users(self) -> list[User]:
        user = User.objects.create(
            username="user",
            name="Demo User",
            is_staff=True,
            is_superuser=True,
            default_ticket_queue=random.choice(self.queues),
        )
        user.set_password("password")
        user.save()
        return [user] + [
            User.objects.create(
                username=self.faker.email(),
                name=self.faker.name(),
                is_staff=True,
                is_superuser=True,
                default_ticket_queue=random.choice(self.queues),
            )
            for _ in range(2, random.randint(3, 8))
        ]

    def handle(
        self,
        *,
        teams_data: Path,
        verbosity: int,
        settings: str,
        pythonpath: str,
        traceback: bool,
        no_color: bool,
        force_color: bool,
        skip_checks: bool,
    ) -> None:
        call_command("flush")
        self.faker = Faker()
        self.teams = self._generate_teams(teams_data)
        self.queues = self._generate_queues()
        self.default_queue = self.queues[0]
        self.escalated_queue = self.queues[1]
        self.users = self._generate_users()

        for day in COMP_DAYS:
            self.simulate_day(day)

        self.stdout.write(self.style.SUCCESS("Successfully generated data"))

    def _generate_new_tickets(self, chance: float, chance_multiple: float) -> None:
        for team in Team.objects.all():
            if random.random() < chance:
                if (
                    team.tickets.filter(resolved_at__isnull=True).count() == 0
                    or random.random() < chance_multiple
                ):
                    team.tickets.create(
                        title=self.faker.sentence(),
                        description=self.faker.text(),
                        queue=self.default_queue,
                        opened_by=random.choice(self.users),
                    )

    def _assign_free_users(self) -> None:
        for user in User.objects.all():
            if user.tickets.filter(resolved_at__isnull=True).count() == 0:
                # Naively assume that the user only gets ticket from their default queue
                # Also assume that a user only picks up one ticket at a time.
                assert user.default_ticket_queue
                ticket = (
                    user.default_ticket_queue.tickets
                    .filter(resolved_at__isnull=True)
                    .filter(assignee__isnull=True)
                    .first()
                )
                if ticket:
                    ticket.assignee = user
                    ticket.save()

    def _ticket_actions(self) -> None:
        for ticket in Ticket.objects.filter(
            assignee__isnull=False, resolved_at__isnull=True
        ):
            if ticket.queue == self.default_queue and random.random() < 0.2:
                ticket.queue = self.escalated_queue
                ticket.assignee = None
                ticket.save()
                continue

            assert ticket.assignee

            if random.random() < 0.1:
                ticket.mark_resolved(ticket.assignee)
                continue

            if random.random() < 0.5:
                ticket.comments.create(
                    content=self.faker.text(),
                    author=ticket.assignee,
                )

    def simulate_day(self, day: datetime.date) -> None:
        current_time = datetime.datetime.combine(day, COMP_OPEN_TIME)
        # Offset time so that the first event is not at exactly 9am
        current_time += datetime.timedelta(seconds=random.randint(30, 600))
        while current_time.time() < COMP_CLOSE_TIME:
            with freezegun.freeze_time(current_time):
                self._ticket_actions()
                self._assign_free_users()
                self._generate_new_tickets(0.05, 0.05)

            # Advance time
            current_time += datetime.timedelta(seconds=random.randint(30, 600))
