# Generated by Django 4.0.3 on 2022-04-05 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0097_alter_availability_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='realm',
            name='is_default',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 5, 16, 22, 45, 409767)),
        ),
    ]