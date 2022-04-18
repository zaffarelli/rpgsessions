# Generated by Django 4.0.3 on 2022-04-18 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0146_alter_profile_hair_style_alter_profile_mouth_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='full_run_duration',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='campaign',
            name='toc',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
    ]
