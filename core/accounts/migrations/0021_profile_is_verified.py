# Generated by Django 5.0.1 on 2024-04-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0020_rename_username_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
