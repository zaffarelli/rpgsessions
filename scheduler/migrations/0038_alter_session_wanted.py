# Generated by Django 4.0.3 on 2022-03-21 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0037_session_wanted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='wanted',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
