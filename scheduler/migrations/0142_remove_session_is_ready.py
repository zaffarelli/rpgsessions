# Generated by Django 4.0.3 on 2022-04-15 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0141_profile_hair_style_profile_mouth_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='is_ready',
        ),
    ]
