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

    def __str__(self):
        return f'{self.title} ({self.mj})'
    

class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'mj']