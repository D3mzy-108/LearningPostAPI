# Generated by Django 4.2 on 2025-04-29 12:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learningpost_professional', '0003_test_testquestion_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionalorganization',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
