# Generated by Django 4.0.3 on 2022-04-02 22:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0081_alter_availability_when_alter_game_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 3, 0, 26, 6, 612400)),
        ),
    ]
