from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField
from scheduler.models.game import Game
from scheduler.models.profile import Profile
import json


class Campaign(models.Model):
    title = models.CharField(max_length=256)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    mj = models.ForeignKey(Profile, on_delete=models.CASCADE)
    acronym = models.CharField(max_length=6, default='')
    description = models.TextField(max_length=2048, default='', blank=True)
    wanted = models.CharField(max_length=64, default='', blank=True)
    alpha = ColorField(default='#666666')
    toc = models.TextField(max_length=2048, default='', blank=True)
    full_run_duration = models.PositiveIntegerField(default=0, blank=True)
    is_visible = models.BooleanField(default=False, blank=True)
    is_finished = models.BooleanField(default=False, blank=True)


    def __str__(self):
        return f'{self.title} ({self.mj})'

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

    @property
    def sessions_summary(self):
        from scheduler.views.organizer import gimme_session
        from scheduler.models.session import Session
        list = []
        episodes = Session.objects.filter(campaign=self).order_by("-date_start")
        if len(episodes) > 0:
            for episode in episodes:
                list.append(gimme_session(episode))
        return list


    @property
    def wanted_list(self):
        from scheduler.views.organizer import gimme_profile
        wanted = self.wanted
        list = []
        if len(wanted) > 0:
            wanted_players = wanted.split(';')
            for wp in wanted_players:
                _set = Profile.objects.filter(pk=int(wp))
                if len(_set) == 1:
                    this = _set.first()
                    list.append(gimme_profile(this.id))
        return list


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'mj', 'wanted']
    list_filter = ['game', 'mj']