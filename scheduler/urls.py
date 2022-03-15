from django.urls import path, re_path
from scheduler.views.base import index

urlpatterns = [
    re_path(r'^$', index, name='index'),
]

