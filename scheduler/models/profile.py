from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from scheduler.models.realm import Realm
from colorfield.fields import ColorField
import json


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True)
    is_girl = models.BooleanField(default=False)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def u_u(self):
        return self.user.username

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

    @property
    def following(self):
        from scheduler.models.follower import Follower
        list = []
        all = Follower.objects.filter(profile=self)
        for x in all:
            list.append(x.target.to_json)
        return list

    @property
    def groupies(self):
        from scheduler.models.follower import Follower
        list = []
        all = Follower.objects.filter(target=self)
        for x in all:
            list.append(x.profile.to_json)
        return list


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['u_u','nickname','realm', 'presentation']
