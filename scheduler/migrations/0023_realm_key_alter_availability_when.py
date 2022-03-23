# Generated by Django 4.0.3 on 2022-03-22 22:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0022_alter_availability_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='realm',
            name='key',
            field=models.CharField(default='JdR$31', max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 22, 23, 49, 50, 725027)),
        ),
    ]
