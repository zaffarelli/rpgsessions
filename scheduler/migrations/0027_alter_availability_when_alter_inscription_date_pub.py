# Generated by Django 4.0.3 on 2022-03-19 01:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0026_alter_availability_when_alter_inscription_date_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 19, 1, 50, 48, 567771, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 1, 50, 48, 567123, tzinfo=utc)),
        ),
    ]
