from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField

class Game(models.Model):
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=32, default='')
    acronym = models.CharField(max_length=6, default='')
    description = models.TextField(max_length=2048, default='', blank=True)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.name} ({self.version})'

class GameAdmin(admin.ModelAdmin):
    ordering = ['name', 'version']
    list_display = ['name', 'version', 'acronym', 'alpha', 'beta', 'gamma', 'description']


