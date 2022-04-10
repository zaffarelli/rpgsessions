# Generated by Django 4.0.3 on 2022-03-29 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0054_game_mj_alter_availability_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='wanted',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 29, 12, 6, 35, 362453)),
        ),
    ]