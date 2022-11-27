from django import forms
from scheduler.models.profile import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        hidden = ["id", "padid"]
