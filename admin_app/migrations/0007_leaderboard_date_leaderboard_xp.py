# Generated by Django 4.2 on 2025-05-08 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0006_library_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboard',
            name='date',
            field=models.DateField(default=datetime.date(2025, 5, 8), null=True),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='xp',
            field=models.IntegerField(default=0),
        ),
    ]
