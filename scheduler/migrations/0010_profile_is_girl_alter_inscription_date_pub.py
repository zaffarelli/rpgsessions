# Generated by Django 4.0.3 on 2022-03-18 03:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_alter_inscription_date_pub'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_girl',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 18, 4, 52, 8, 182525)),
        ),
    ]