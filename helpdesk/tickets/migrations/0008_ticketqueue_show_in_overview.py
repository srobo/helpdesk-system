# Generated by Django 3.2.18 on 2023-04-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_ticketqueue_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketqueue',
            name='show_in_overview',
            field=models.BooleanField(default=True, verbose_name='Show in Display Overview'),
        ),
    ]
