from django import forms
from scheduler.models.profile import Profile
from colorfield.fields import ColorField

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
