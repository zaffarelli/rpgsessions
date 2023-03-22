from django.db import models
from django.contrib import admin
from scheduler.models.abstractsession import AbstractSession
from scheduler.models.session import Session
import json


class Spot(AbstractSession):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def me(self):
        str = f"Ghost Session #{self.id:04} for [{self.session.title}]"
        return str

    def __str__(self):
        return self.me

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class SpotAdmin(admin.ModelAdmin):
    ordering = ['session']
    list_display = ['me', 'session']
