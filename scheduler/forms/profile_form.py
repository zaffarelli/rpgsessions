from django import forms
from scheduler.models.profile import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["face_style", "hair_style", "mouth_style"]
        hidden = ["id", "padid"]
