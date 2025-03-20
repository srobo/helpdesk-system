# Generated by Django 4.2.11 on 2025-03-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0005_alter_team_options_teamattendanceevent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teamattendanceevent",
            name="comment",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="teamattendanceevent",
            name="type",
            field=models.TextField(
                choices=[
                    ("ARRIVED", "Arrived"),
                    ("LEFT", "Left"),
                    ("DELAYED", "Delayed"),
                    ("DROPPED_OUT", "Dropped Out"),
                    ("UNKNOWN", "Unknown"),
                ],
                max_length=11,
            ),
        ),
    ]
