# Generated by Django 4.0.3 on 2022-03-18 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0015_alter_inscription_date_pub_availability'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='availability',
            options={'verbose_name_plural': 'availabilities'},
        ),
        migrations.AlterField(
            model_name='availability',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 18, 15, 11, 28, 117973)),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 18, 15, 11, 28, 117954)),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 18, 15, 11, 28, 117047)),
        ),
    ]
