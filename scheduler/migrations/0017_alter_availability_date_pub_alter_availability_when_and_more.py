# Generated by Django 4.0.3 on 2022-03-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0016_alter_availability_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='date_pub',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='when',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='date_pub',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
