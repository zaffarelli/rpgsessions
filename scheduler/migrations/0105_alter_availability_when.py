# Generated by Django 4.0.3 on 2022-04-05 16:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0104_alter_availability_when_alter_session_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 5, 18, 15, 45, 645183)),
        ),
    ]
