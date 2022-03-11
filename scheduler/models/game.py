from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=2048, default='', blank=True)

    

