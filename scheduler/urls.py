from django.urls import path, re_path
from scheduler.views.base import index, display_day

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>[\w+]+)/$', display_day, name='display_day'),
]

