# Generated by Django 4.0.3 on 2022-04-03 20:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0090_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 3, 22, 52, 20, 421443)),
        ),
    ]
