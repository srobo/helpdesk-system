# Generated by Django 3.2.18 on 2023-03-26 18:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_allow_default_ticket_queue_to_be_blank"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="onboarded_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
