# Generated by Django 4.0.3 on 2022-03-21 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_alter_availability_date_pub'),
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
    ]
