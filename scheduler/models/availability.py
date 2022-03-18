from django.db import models
from django.contrib import admin
from django.utils.timezone import now
from datetime import datetime
from scheduler.models.profile import Profile
from scheduler.models.session import Session
import json


class Availability(models.Model):
    class Meta:
        verbose_name_plural = 'availabilities'
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    when = models.DateField(default=now())
    date_pub = models.DateTimeField(auto_now=now())

    def __str__(self):
        return f'{self.profile.nickname} -> {self.when.strftime("%Y-%m-%d")}'

    @property
    def this(self):
        return self.__str__

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['this', 'when', 'date_pub', 'profile']