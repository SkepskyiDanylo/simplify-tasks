# Generated by Django 5.1.4 on 2025-03-19 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0015_worker_location_alter_worker_facebook_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="workers",
        ),
        migrations.AddField(
            model_name="team",
            name="leader",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="leader_of",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="worker",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="workers",
                to="manager.team",
            ),
        ),
    ]
