# Generated by Django 4.2.2 on 2024-02-22 12:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0017_profile_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="email",
        ),
    ]
