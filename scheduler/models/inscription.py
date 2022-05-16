from django.db import models
from django.contrib import admin
from datetime import datetime
from django.utils import timezone
from scheduler.models.profile import Profile
from scheduler.models.session import Session
import json


class Inscription(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now=timezone.now())
    pending = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.profile.nickname} -> "{self.session}"'

    @property
    def this(self):
        return self.__str__

    def propagate(self):
        if self.session.date_start is not None:
            from scheduler.models.availability import Availability
            ons = Availability.objects.filter(when=self.session.date_start, profile=self.profile)
            for x in ons:
                x.delete()

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['this', 'date_pub', 'session', 'profile']
    list_filter = ['profile', 'session']
