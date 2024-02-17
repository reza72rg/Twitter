# Generated by Django 4.2.2 on 2024-02-14 17:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("twitter", "0003_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="approach",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="comment",
            name="message",
            field=models.TextField(default=22),
            preserve_default=False,
        ),
    ]