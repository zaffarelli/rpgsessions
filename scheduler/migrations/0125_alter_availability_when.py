# Generated by Django 4.0.3 on 2022-04-10 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0124_realm_full_link_alter_availability_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 4, 10, 17, 46, 25, 71226)),
        ),
    ]
