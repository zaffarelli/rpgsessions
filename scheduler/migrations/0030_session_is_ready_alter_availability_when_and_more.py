# Generated by Django 4.0.3 on 2022-03-19 04:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0029_session_max_episodes_alter_availability_when_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='is_ready',
            field=models.BooleanField(default=False, verbose_name='ok'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(default=datetime.datetime(2022, 3, 19, 4, 45, 3, 836467, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 4, 45, 3, 835945, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='level',
            field=models.CharField(choices=[('0', 'Débutants'), ('1', 'Tranquille'), ('2', 'Intermédiaire'), ('3', 'Difficile'), ('4', 'Chevronnés')], default='0', max_length=16),
        ),
    ]