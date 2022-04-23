from django.urls import re_path
from scheduler.views.base import index, display_day, display_month, display_session, display_user, \
    display_overlay, toggle_follower, simple_toggle, delete_session, display_campaign, \
    delete_campaign, display_game, validate_game, validate_session, validate_campaign, validate_profile
from scheduler.views.misc import who, register_submit, handle_invitation
from scheduler.views.page import propositions, members, campaigns
from django.contrib.auth.views import LogoutView

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>\w+)/$', display_day, name='display_day'),
    re_path(r'^ajax/display/month/(?P<slug>\w+)/$', display_month, name='display_month'),
    re_path(r'^ajax/display/session_details/(?P<id>\d+)/$', display_session, name='display_session'),
    re_path(r'^ajax/display/user/(?P<id>\d+)/$', display_user, name='display_user'),
    re_path(r'^ajax/display/game/(?P<id>\d+)/$', display_game, name='display_game'),
    re_path(r'^ajax/display/propositions/$', propositions, name='propositions'),
    re_path(r'^ajax/display/members/$', members, name='members'),
    re_path(r'^ajax/display/campaigns/$', campaigns, name='campaigns'),
    re_path(r'^ajax/display/campaign/(?P<id>\d+)/$', display_campaign, name='display_campaign'),
    re_path(r'^invite/(?P<slug>\w+)/$', handle_invitation, name='handle_invitation'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/(?P<option>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/toggle/toggle_follower/(?P<id>\d+)/$', toggle_follower, name='toggle_follower'),
    re_path(r'^ajax/toggle/(?P<action>\w+)/(?P<param>\w+)/$', simple_toggle, name='simple_toggle'),
    re_path(r'^ajax/logout/$', LogoutView.as_view(), name="logout"),
    re_path(r'^ajax/action/model_edit/game/(?P<pk>\d+)/$', validate_game, name='valid_game'),
    re_path(r'^ajax/action/model_edit/session/(?P<pk>\d+)/$', validate_session, name='validate_session'),
    re_path(r'^ajax/action/model_edit/profile/(?P<pk>\d+)/$', validate_profile, name='validate_profile'),
    re_path(r'^ajax/action/model_edit/campaign/(?P<pk>\d+)/$', validate_campaign, name='validate_campaign'),
    re_path(r'^ajax/action/session_delete/(?P<pk>\d+)/$', delete_session, name='delete_session'),
    re_path(r'^ajax/action/session_campaign/(?P<pk>\d+)/$', delete_campaign, name='delete_campaign'),
    re_path(r'^register_submit/$', register_submit, name="register_submit"),
    re_path(r'^who/(?P<pk>\d+)/$', who, name="who"),

]
