# Generated by Django 4.0.3 on 2022-04-20 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0150_game_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='is_visible',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
