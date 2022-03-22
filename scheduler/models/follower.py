from django.db import models
from django.contrib import admin
from django.utils.timezone import now
from datetime import datetime
from scheduler.models.profile import Profile
import json


class Follower(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followed')
    date_pub = models.DateTimeField(auto_now=now())

    def __str__(self):
        return f'{self.profile.nickname} follows {self.target.nickname}'

    @property
    def this(self):
        return self.__str__

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class FollowerAdmin(admin.ModelAdmin):
    list_display = ['this', 'profile', 'date_pub', 'target']
