# Generated by Django 4.1.6 on 2023-02-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_remove_contract_status_contract_signed_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_status",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
