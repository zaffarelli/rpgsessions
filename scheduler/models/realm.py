from django.db import models
from django.contrib import admin
import json


class Realm(models.Model):
    name = models.CharField(max_length=256, unique=True)
    key = models.CharField(max_length=256, default='JdR$31', unique=True)
    description = models.TextField(max_length=2048, default='', blank=True)

    def __str__(self):
        return self.name

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

    @property
    def invite_link(self):
        from hashlib import blake2s
        h = blake2s()
        h.update(bytes(f'{self.key}','UTF-8'))
        res = h.hexdigest()
        return res


class RealmAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'description', 'invite_link']
