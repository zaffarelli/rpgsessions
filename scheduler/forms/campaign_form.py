from django import forms
from scheduler.models.campaign import Campaign
from colorfield.fields import ColorField

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = "__all__"
