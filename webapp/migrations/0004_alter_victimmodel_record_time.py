# Generated by Django 4.0.6 on 2022-12-01 18:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_victimmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='victimmodel',
            name='record_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
