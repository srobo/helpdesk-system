# Generated by Django 4.2.11 on 2024-04-10 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0004_add_team_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["tla"]},
        ),
        migrations.AlterField(
            model_name="team",
            name="pit_location",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="teams.teampitlocation"),
        ),
    ]
