# Generated by Django 4.0.3 on 2022-03-19 11:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0033_alter_availability_when_alter_inscription_date_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 19, 11, 29, 12, 434401, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 11, 29, 12, 433899, tzinfo=utc)),
        ),
    ]
