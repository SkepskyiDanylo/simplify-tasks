# Generated by Django 5.1.4 on 2025-01-03 20:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0006_alter_worker_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="hire_date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="worker",
            name="last_activity",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
