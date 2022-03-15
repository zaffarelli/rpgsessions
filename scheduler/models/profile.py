from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from scheduler.models.realm import Realm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def u_u(self):
        return self.user.username


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['u_u','nickname','realm', 'presentation']
