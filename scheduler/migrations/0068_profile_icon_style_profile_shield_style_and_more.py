# Generated by Django 4.0.3 on 2022-04-02 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0067_alter_availability_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='icon_style',
            field=models.CharField(choices=[('disk', 'Medium disk')], default='disk', max_length=256),
        ),
        migrations.AddField(
            model_name='profile',
            name='shield_style',
            field=models.CharField(choices=[('mid', 'West-East'), ('quad', 'NW NE SE SW')], default='mid', max_length=256),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 2, 18, 4, 18, 146011)),
        ),
    ]
