# Generated by Django 4.0.3 on 2022-04-02 21:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0069_profile_svg_artefact_alter_availability_when_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 2, 23, 56, 23, 481412)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon_style',
            field=models.CharField(choices=[('disk', 'Disque'), ('coins', 'Trois deniers'), ('cross', 'Croix'), ('claws', 'Griffure'), ('diamond', 'Losange')], default='disk', max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shield',
            field=models.CharField(default='shield_base', max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shield_style',
            field=models.CharField(choices=[('mid', 'Gauche et droite'), ('quad', 'Quadrants NO, NE, SE, SW en damier'), ('half', 'Haut et bas séparés')], default='mid', max_length=256),
        ),
    ]
