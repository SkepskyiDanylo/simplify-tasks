# Generated by Django 5.1.4 on 2024-12-31 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0003_tag_task_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="information",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="worker",
            name="phone_number",
            field=models.CharField(
                default=111111111,
                max_length=15,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'",
                        regex="^\\+?1?\\d{9,15}$",
                    )
                ],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="worker",
            name="profile_picture",
            field=models.ImageField(
                default="profile_pictures/default.jpg", upload_to="profile_pictures/"
            ),
        ),
    ]
