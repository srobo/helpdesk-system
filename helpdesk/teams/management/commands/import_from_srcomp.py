import requests
from django.core.management.base import BaseCommand, CommandParser

from teams.models import Team, TeamPitLocation

DEFAULT_SRCOMP = "https://srcomp.studentrobotics.org/comp-api"

class Command(BaseCommand):
    help = "Import teams and pit locations from SRComp"  # noqa: A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--srcomp_url", type=str, default=DEFAULT_SRCOMP)

    def handle(
        self,
        *,
        srcomp_url: str,
        verbosity: int,
        settings: str,
        pythonpath: str,
        traceback: bool,
        no_color: bool,
        force_color: bool,
        skip_checks: bool,
    ) -> None:
        self._import_pit_locations(srcomp_url)
        self._import_teams(srcomp_url)
        self.stdout.write("Imported teams and pits")

    def _import_pit_locations(self, srcomp_url: str) -> None:
        resp = requests.get(f"{srcomp_url}/locations", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        for slug, location_data in data["locations"].items():
            TeamPitLocation.objects.get_or_create(
                slug=slug,
                defaults={"name": location_data["display_name"]},
            )

    def _import_teams(self, srcomp_url: str) -> None:
        resp = requests.get(f"{srcomp_url}/teams", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        for tla, team_data in data["teams"].items():
            team, created = Team.objects.select_related("pit_location").get_or_create(
                tla=tla,
                defaults={
                    "name": team_data["name"],
                    "is_rookie": team_data.get("rookie", False),
                    "pit_location": TeamPitLocation.objects.get(slug=team_data["location"]["name"]),
                },
            )

            # If not created, synchronise the pit locations.
            if not created and team.pit_location.slug != team_data["location"]["name"]:
                team.pit_location = TeamPitLocation.objects.get(slug=team_data["location"]["name"])
                team.save(update_fields=["pit_location"])
