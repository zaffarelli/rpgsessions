from django.db import models
from django.contrib import admin


class Realm(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=2048, default='', blank=True)

    def __str__(self):
        return self.name

class RealmAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name','description']



