# Generated by Django 4.0.3 on 2022-04-06 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0115_alter_availability_when_alter_profile_icon_style'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='icon_style',
            new_name='iconstyle',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='shield_style',
            new_name='shieldstyle',
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 6, 11, 53, 25, 88277)),
        ),
    ]
