# Generated by Django 4.0.3 on 2022-03-18 02:34

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_alter_session_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='alpha',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='beta',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='gamma',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='session',
            name='alpha',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='session',
            name='beta',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddField(
            model_name='session',
            name='gamma',
            field=colorfield.fields.ColorField(default='#666666', image_field=None, max_length=18, samples=None),
        ),
    ]