from django import forms
from scheduler.models.game import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"
        hidden = ["id"]
