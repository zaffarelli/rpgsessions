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
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.title} ({self.mj})'


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'mj']