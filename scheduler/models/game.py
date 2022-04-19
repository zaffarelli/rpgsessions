from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField
from scheduler.models.profile import Profile
import json

SYSTEMS = (
    ('type1', 'Chaosium'),
    ('type2', 'd20'),
    ('type3', 'Rein*Hagen'),
    ('type4', 'FICS'),
    ('type666', 'aucun/autre')
)


class Game(models.Model):
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=32, default='')
    acronym = models.CharField(max_length=32, default='')
    system = models.CharField(choices=SYSTEMS, max_length=32, default='type666')
    description = models.TextField(max_length=2048, default='', blank=True)
    mj = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.name} ({self.version})'

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

    @property
    def svg_artefact(self):
        artefact = {'type1': 0.0, 'type2': 0.0, 'type3': 0.0, 'type4': 0.0, 'type666': 0.0, self.system: 1.0}
        return artefact


class GameAdmin(admin.ModelAdmin):
    ordering = ['name', 'version']
    list_display = ['name', 'version', 'acronym', 'mj', 'alpha', 'beta', 'gamma', 'description']
