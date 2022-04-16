from django import forms
from scheduler.models.session import Session
from django.forms.widgets import NumberInput
from colorfield.fields import ColorField


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = "__all__"

    date_start = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=False)
    time_start = forms.TimeField(widget=NumberInput(attrs={'type': 'time'}))
