# Generated by Django 4.0.3 on 2022-03-21 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_remove_session_camp'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduler.campaign'),
        ),
    ]
