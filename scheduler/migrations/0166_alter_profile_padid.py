# Generated by Django 4.0.3 on 2022-11-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0165_profile_padid_alter_profile_hair_style_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='padid',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
    ]
