from django.urls import path, re_path
from scheduler.views.base import index, display_day, display_month, display_session

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>[\w+]+)/$', display_day, name='display_day'),
    re_path(r'^ajax/display/month/(?P<slug>[\w+]+)/$', display_month, name='display_month'),
    re_path(r'^ajax/display/session_details/(?P<id>[\d])/$', display_session, name='display_session'),
]

