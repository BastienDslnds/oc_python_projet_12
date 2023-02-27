# Generated by Django 4.1.6 on 2023-02-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_alter_client_date_created_alter_client_date_updated_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="date_updated",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="contract",
            name="date_updated",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="date_updated",
            field=models.DateField(auto_now_add=True),
        ),
    ]