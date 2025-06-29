# Generated by Django 4.2 on 2025-03-16 17:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_app', '0002_remove_library_bookmarked_remove_quest_bookmarked'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quest',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
