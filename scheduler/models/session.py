from django.db import models
from django.contrib import admin
from datetime import datetime, timedelta
from scheduler.models.realm import Realm
from scheduler.models.game import Game
from scheduler.models.profile import Profile
from django.contrib.auth.models import User
from colorfield.fields import ColorField
import json
from scheduler.utils.mechanics import ADV_LEVEL


class Session(models.Model):
    title = models.CharField(max_length=256)
    episode = models.PositiveIntegerField(default=1)
    max_episodes = models.PositiveIntegerField(default=1)
    mj = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    campaign = models.CharField(max_length=256, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2048, default='', blank=True)
    date_start = models.DateField(default=datetime.now)
    time_start = models.TimeField(default=datetime.now)
    duration = models.PositiveIntegerField(default=4)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=True)
    mandatory_spots = models.PositiveIntegerField(default=4)
    optional_spots = models.PositiveIntegerField(default=0)
    newbies_allowed = models.BooleanField(default=True, verbose_name='noobs')
    one_shot_adventure = models.BooleanField(default=True, verbose_name='oneshot')
    level = models.CharField(max_length=16, default='0', choices=ADV_LEVEL)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')
    is_ready = models.BooleanField(default=False, verbose_name='ok')

    def __str__(self):
        return f"{self.title} ({self.episode})"

    @property
    def date_end(self):
        res = datetime.combine(self.date_start, self.time_start)
        res = res + timedelta(hours=self.duration)
        return res

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class SessionAdmin(admin.ModelAdmin):
    ordering = ['date_start', 'time_start']
    list_display = ['title', 'date_start', 'time_start','is_ready', 'duration', 'date_end', 'mj', 'newbies_allowed',
                    'one_shot_adventure', 'campaign']
    search_fields = ['title', 'description']
    list_filter = ['campaign', 'level', 'game']
