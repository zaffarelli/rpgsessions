from django import forms
from scheduler.models.campaign import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = "__all__"
