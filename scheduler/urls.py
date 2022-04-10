from django.urls import path, re_path
from scheduler.views.base import index, display_day, display_month, display_session, display_user, handle_invitation, \
    display_overlay, toggle_follower, simple_toggle, show_done, delete_session, register_submit
from scheduler.views.session import  SessionUpdateView #, SessionCreateView,SessionDeleteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>\w+)/$', display_day, name='display_day'),
    re_path(r'^ajax/display/month/(?P<slug>\w+)/$', display_month, name='display_month'),
    re_path(r'^ajax/display/session_details/(?P<id>\d+)/$', display_session, name='display_session'),
    re_path(r'^ajax/display/user/(?P<id>\d+)/$', display_user, name='display_user'),
    re_path(r'^invite/(?P<slug>\w+)/$', handle_invitation, name='handle_invitation'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/(?P<option>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/toggle/toggle_follower/(?P<id>\d+)/$', toggle_follower, name='toggle_follower'),
    re_path(r'^ajax/toggle/(?P<action>\w+)/(?P<param>\w+)/$', simple_toggle, name='simple_toggle'),
    re_path(r'^ajax/logout/$', LogoutView.as_view(), name="logout"),
    # re_path(r'^ajax/action/session_create/$', SessionCreateView.as_view(), name="create_session"),
    re_path(r'^ajax/action/session_edit/(?P<pk>\d+)/$', SessionUpdateView.as_view(), name='update_session'),
    re_path(r'^ajax/action/session_delete/(?P<pk>\d+)/$', delete_session, name='delete_session'),
    # re_path(r'^ajax/action/session_delete/(?P<pk>\d+)/$', SessionDeleteView.as_view(), name='delete_session'),
    # re_path(r'^ajax/action/session_update/(?P<pk>\d+)/$', update, name="show_done"),
    re_path(r'^register_submit/$', register_submit, name="register_submit"),
]
