# Generated by Django 4.0.3 on 2022-04-05 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0098_realm_is_default_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 5, 16, 22, 58, 836861)),
        ),
    ]
