from django.db import models
from django.contrib import admin
import datetime


class Session(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=2048, default='', blank=True)
    date_start = models.DateField(default=datetime.today)
    time_start = models.DateField(default=datetime.now)
    duration = models.PositiveIntegerField(default=4)

    @property
    def __str__(self):
        return self.title

    @property
    def time_end(self):
        return self.time_start + datetime.timedelta(hours=self.duration)


class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_start', 'duration']
