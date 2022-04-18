from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from scheduler.forms.campaign_form import CampaignForm
from scheduler.models.campaign import Campaign
from scheduler.mixins.ajaxfromresponse import AjaxFromResponseMixin


class CampaignDetailView(AjaxFromResponseMixin, DetailView):
    model = Campaign
    context_object_name = 'c'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CampaignUpdateView(AjaxFromResponseMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    context_object_name = 'c'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('display_campaign', kwargs={'id': self.object.pk})

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(SessionUpdateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = SessionForm(self.request.POST, instance=self.object)
    #     else:
    #         context['form'] = SessionForm(instance=self.object)
    #     return context