from django.urls import path, re_path
from scheduler.views.base import index, display_day, display_month, display_session, display_user, handle_invitation, \
    display_overlay, toggle_follower

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>[\w+]+)/$', display_day, name='display_day'),
    re_path(r'^ajax/display/month/(?P<slug>[\w+]+)/$', display_month, name='display_month'),
    re_path(r'^ajax/display/session_details/(?P<id>[\d])/$', display_session, name='display_session'),
    re_path(r'^ajax/display/user/(?P<id>[\d])/$', display_user, name='display_user'),
    re_path(r'^invite/(?P<slug>[\w+]+)/$', handle_invitation, name='handle_invitation'),
    re_path(r'^ajax/overlay/(?P<slug>[\w+]+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/toggle/toggle_follower/(?P<id>[\d])/$', toggle_follower, name='toggle_follower'),
]
