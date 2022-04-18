from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField
from scheduler.models.game import Game
from scheduler.models.profile import Profile
import json


class Campaign(models.Model):
    title = models.CharField(max_length=256)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    mj = models.ForeignKey(Profile, on_delete=models.CASCADE)
    acronym = models.CharField(max_length=6, default='')
    description = models.TextField(max_length=2048, default='', blank=True)
    wanted = models.CharField(max_length=64, default='', blank=True)
    alpha = ColorField(default='#666666')
    toc = models.TextField(max_length=2048, default='', blank=True)
    full_run_duration = models.PositiveIntegerField(default=0, blank=True)


    def __str__(self):
        return f'{self.title} ({self.mj})'

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'mj']