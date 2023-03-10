# Generated by Django 4.1.6 on 2023-02-28 08:12

import crm.events.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_eventstatus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_status",
            field=models.ForeignKey(
                default=crm.events.models.EventStatus.get_default_pk,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.eventstatus",
            ),
        ),
        migrations.AlterField(
            model_name="eventstatus",
            name="status",
            field=models.BooleanField(default=False, unique=True),
        ),
    ]
