# Generated by Django 4.0.3 on 2022-04-07 06:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0118_profile_weeks_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 7, 8, 1, 55, 954983)),
        ),
    ]
