from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from scheduler.forms.game_form import GameForm
from scheduler.models.game import Game
from scheduler.mixins.ajaxfromresponse import AjaxFromResponseMixin


# class GameDetailView(AjaxFromResponseMixin, DetailView):
#     model = Game
#     context_object_name = 'c'


# class GameUpdateView(AjaxFromResponseMixin, UpdateView):
#     model = Game
#     form_class = GameForm
#     context_object_name = 'c'
#     template_name_suffix = '_update_form'
#
#     def get_success_url(self):
#         return reverse('display_game', kwargs={'id': self.object.pk})
#
#     def get_context_data(self, **kwargs):
#         context = super(GameUpdateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['form'] = GameForm(self.request.POST, instance=self.object)
#             context['callback'] = "Yo man"
#         else:
#             context['form'] = GameForm(instance=self.object)
#         return context