# Generated by Django 3.2.17 on 2023-02-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0001_create_ticket_models"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticketqueue",
            options={"ordering": ["-display_priority", "name"]},
        ),
        migrations.AddField(
            model_name="ticketqueue",
            name="display_priority",
            field=models.PositiveSmallIntegerField(default=1, verbose_name="Display Priority"),
        ),
    ]
