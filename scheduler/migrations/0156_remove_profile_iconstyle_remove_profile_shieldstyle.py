# Generated by Django 4.0.3 on 2022-05-05 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0155_rename_mail_daily_profile_mail_cyber_postit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='iconstyle',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='shieldstyle',
        ),
    ]
