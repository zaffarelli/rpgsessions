# Generated by Django 4.0.3 on 2022-03-15 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_session_campaign_remove_session_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='campaign',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='session',
            name='level',
            field=models.CharField(choices=[('0', 'Débutants'), ('1', 'Bas niveaux'), ('2', 'Niveaux intermédiaires'), ('3', 'Haut niveaux'), ('4', 'Chevronnés')], default='0', max_length=16),
        ),
        migrations.AddField(
            model_name='session',
            name='newbies_allowed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='session',
            name='one_shot_adventure',
            field=models.BooleanField(default=True),
        ),
    ]