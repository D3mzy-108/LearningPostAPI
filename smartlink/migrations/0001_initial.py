# Generated by Django 4.2 on 2025-03-16 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SmartLinkKB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('definition', models.TextField()),
            ],
            options={
                'verbose_name': 'SmartLinkKB',
                'verbose_name_plural': 'SmartLinksKB',
            },
        ),
    ]
