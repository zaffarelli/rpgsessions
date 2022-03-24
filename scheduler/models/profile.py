from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from scheduler.models.realm import Realm
from colorfield.fields import ColorField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True)
    is_girl = models.BooleanField(default=False)
    shield = models.CharField(max_length=256, default='gamemaster_shield')
    silhouette = models.CharField(max_length=256, default='player')
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.nickname}*'

    @property
    def u_u(self):
        return self.user.username

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        import json
        return json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))

    @property
    def following(self):
        from scheduler.models.follower import Follower
        from scheduler.utils.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(profile=self)
        for x in all:
            list.append(gimme_profile(x.target.id))
        return list

    @property
    def groupies(self):
        from scheduler.models.follower import Follower
        from scheduler.utils.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(target=self)
        for x in all:
            list.append(gimme_profile(x.profile.id))
        return list

    @property
    def games_run(self):
        from scheduler.models.session import Session
        all = Session.objects.filter(mj=self)
        return len(all)

    @property
    def silhouette_symbol(self):
        girl = ''
        if self.is_girl:
            girl = '_girl'
        return f"scheduler/svg/{self.silhouette}{girl}.svg"

    @property
    def shield_symbol(self):
        return f"scheduler/svg/{self.shield}.svg"


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['u_u', 'nickname', 'realm', 'games_run', 'shield', 'silhouette', 'presentation']
