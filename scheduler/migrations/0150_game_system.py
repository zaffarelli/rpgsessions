# Generated by Django 4.0.3 on 2022-04-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0149_alter_game_acronym'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='system',
            field=models.CharField(choices=[('type1', 'Chaosium'), ('type2', 'd20'), ('type3', 'Rein*Hagen'), ('type4', 'FICS'), ('type666', 'aucun/autre')], default='type666', max_length=32),
        ),
    ]