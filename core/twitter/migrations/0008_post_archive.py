# Generated by Django 4.2.2 on 2024-02-16 20:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("twitter", "0007_alter_comment_author_alter_dislike_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="archive",
            field=models.BooleanField(default=True),
        ),
    ]
