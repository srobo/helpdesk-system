# Generated by Django 3.2.17 on 2023-02-08 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tickets", "0001_create_ticket_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="resolved_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="resolved_tickets",
                related_query_name="resolved_tickets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="opened_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="opened_tickets",
                related_query_name="opened_tickets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]