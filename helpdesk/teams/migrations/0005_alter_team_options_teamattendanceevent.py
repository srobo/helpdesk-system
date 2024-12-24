# Generated by Django 4.2.11 on 2024-12-24 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0004_add_team_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["tla"]},
        ),
        migrations.CreateModel(
            name="TeamAttendanceEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.TextField(
                        choices=[("AR", "Arrived"), ("LE", "Left"), ("DE", "Delayed"), ("DO", "Dropped Out")],
                        max_length=2,
                    ),
                ),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_attendance_events",
                        related_query_name="team_attendance_events",
                        to="teams.team",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
