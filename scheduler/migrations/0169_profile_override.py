# Generated by Django 4.0.3 on 2022-11-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0168_alter_profile_face_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='override',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
