# Generated by Django 4.0.3 on 2022-03-18 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_inscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 18, 4, 44, 26, 189601)),
        ),
    ]