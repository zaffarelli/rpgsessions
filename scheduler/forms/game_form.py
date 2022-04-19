from django import forms
from scheduler.models.game import Game
from colorfield.fields import ColorField


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"
