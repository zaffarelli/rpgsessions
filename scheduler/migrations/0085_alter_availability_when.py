# Generated by Django 4.0.3 on 2022-04-02 22:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0084_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 3, 0, 29, 30, 276005)),
        ),
    ]
