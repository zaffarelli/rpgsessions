# Generated by Django 4.0.3 on 2022-03-23 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0029_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 23, 1, 46, 37, 663445)),
        ),
    ]
