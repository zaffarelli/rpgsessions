# Generated by Django 4.0.3 on 2022-03-18 03:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_alter_session_mj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pub', models.DateTimeField(default=datetime.datetime(2022, 3, 18, 4, 36, 28, 597859))),
                ('pending', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.profile')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.session')),
            ],
        ),
    ]
