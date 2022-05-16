from django.db import models
from django.contrib import admin
from datetime import datetime, timedelta, time
from scheduler.models.realm import Realm
from scheduler.models.game import Game
from scheduler.models.profile import Profile
from colorfield.fields import ColorField
import json
from scheduler.utils.mechanics import ADV_LEVEL
from scheduler.models.campaign import Campaign


class Session(models.Model):
    title = models.CharField(max_length=512)
    # episode = models.PositiveIntegerField(default=1, blank=True, null=True)
    # max_episodes = models.PositiveIntegerField(default=1, blank=True, null=True)
    mj = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2048, default='', blank=True)
    date_start = models.DateField(default=None, blank=True, null=True)
    time_start = models.TimeField(default=time(hour=18, minute=00, second=00), blank=True)
    duration = models.PositiveIntegerField(default=6, blank=True)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, null=True)
    place = models.CharField(max_length=128, default='', blank=True)
    optional_spots = models.PositiveIntegerField(default=4, blank=True)
    newbies_allowed = models.BooleanField(default=True, verbose_name='noobs', blank=True)
    one_shot_adventure = models.BooleanField(default=True, verbose_name='oneshot', blank=True)
    level = models.CharField(max_length=16, default='0', choices=ADV_LEVEL, blank=True)
    alpha = ColorField(default='#666666', blank=True)
    wanted = models.CharField(max_length=64, default='', blank=True)
    # is_ready = models.BooleanField(default=False, verbose_name='ok', blank=True)
    is_visible = models.BooleanField(default=False, blank=True)
    error_status = models.PositiveIntegerField(default=0)

    def __str__(self):
        str = f"{self.title}"
        if self.campaign:
            str += f" ({self.campaign.title})"
        if self.episode_tag:
            str += f" {self.episode_tag}"
        return str

    @property
    def date_end(self):
        if self.date_start:
            res = datetime.combine(self.date_start, self.time_start)
            res = res + timedelta(hours=self.duration)
        else:
            res = None
        return res

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

    @property
    def wanted_list(self):
        from scheduler.views.organizer import gimme_profile

        if self.campaign:
            wanted = self.campaign.wanted
        else:
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

    @property
    def max_players(self):
        m = self.optional_spots + len(self.wanted_list)
        return m

    @property
    def mandatory_spots(self):
        return len(self.wanted_list)

    @property
    def episode_tag(self):
        n = 0
        i = 0
        t = 0
        if self.campaign is not None:
            episodes = Session.objects.filter(campaign=self.campaign).order_by('date_start', 'time_start')
            t = len(episodes)
            for e in episodes:
                n = n + 1
                if e == self:
                    i = n
        if t == 0:
            return ''
        return f'{i}/{t}'

    def fix_wanted(self):
        print("Fix Wanted")
        from scheduler.models.profile import Profile
        wanted = self.wanted.split(";")
        for w in wanted:
            print("wanted",w, wanted)
            if not w.isdigit():
                wanted.remove(w)
            else:
                profiles = Profile.objects.filter(id=int(w))
                if len(profiles) == 0:
                    wanted.remove(w)
                else:
                    print(f"Session {self.id} wanted list: user found {profiles.first().nickname}")
        wanted_str = ";".join(wanted)
        if wanted_str != self.wanted:
            self.wanted = wanted_str
            self.save()
        return self.wanted

    def gimme_odds(self, d):
        from scheduler.models.inscription import Inscription
        from scheduler.models.availability import Availability
        details = []
        odds = 0.0
        odds_count = 0
        inscriptions = Inscription.objects.filter(session=self)
        realins = inscriptions.values_list('id', flat=True)
        ons = Availability.objects.filter(when=d, absent_mode=False)
        realons = ons.values_list('profile.id', flat=True)
        offs = Availability.objects.filter(when=d, absent_mode=True)
        realoffs = offs.values_list('profile.id', flat=True)

        if self.wanted is None:
            details += ["unknown no wanted"]
        else:
            print(realins)
            print(realons)
            print(realoffs)
            # Dans le cas d'une proposition:
            if self.date_start is None:
                wlist = self.wanted.split(";")
                odds_count = 1 + len(wlist);
                for w in wlist:
                    if w in realins:
                        odds += 1

        return odds, details


class SessionAdmin(admin.ModelAdmin):
    ordering = ['date_start', 'time_start']
    list_display = ['title', 'game', 'campaign', 'date_start', 'time_start', 'max_players', 'duration', 'date_end',
                    'mj', 'newbies_allowed', 'one_shot_adventure', 'episode_tag']
    search_fields = ['title', 'description', 'campaign']
    list_filter = ['game', 'mj', 'campaign', 'level']
