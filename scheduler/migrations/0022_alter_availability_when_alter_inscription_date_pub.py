# Generated by Django 4.0.3 on 2022-03-18 15:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0021_alter_availability_when_alter_inscription_date_pub_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 18, 15, 2, 50, 107741, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 18, 15, 2, 50, 106497, tzinfo=utc)),
        ),
    ]