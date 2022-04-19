from django.urls import path, re_path
from scheduler.views.base import index, display_day, display_month, display_session, display_user, handle_invitation, \
    display_overlay, toggle_follower, simple_toggle, show_done, delete_session, register_submit, display_campaign, delete_campaign, propositions, display_game
from scheduler.views.misc import who
from scheduler.views.game import GameUpdateView
from scheduler.views.session import SessionUpdateView
from scheduler.views.profile import ProfileUpdateView
from scheduler.views.campaign import CampaignUpdateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^ajax/display/dayzoom/(?P<slug>\w+)/$', display_day, name='display_day'),
    re_path(r'^ajax/display/month/(?P<slug>\w+)/$', display_month, name='display_month'),
    re_path(r'^ajax/display/session_details/(?P<id>\d+)/$', display_session, name='display_session'),
    re_path(r'^ajax/display/user/(?P<id>\d+)/$', display_user, name='display_user'),
    re_path(r'^ajax/display/game/(?P<id>\d+)/$', display_game, name='display_game'),
    re_path(r'^ajax/display/propositions/$', propositions, name='propositions'),
    re_path(r'^ajax/display/campaign/(?P<id>\d+)/$', display_campaign, name='display_campaign'),
    re_path(r'^invite/(?P<slug>\w+)/$', handle_invitation, name='handle_invitation'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/overlay/(?P<slug>\w+)/(?P<param>\w+)/(?P<option>\w+)/$', display_overlay, name='display_overlay'),
    re_path(r'^ajax/toggle/toggle_follower/(?P<id>\d+)/$', toggle_follower, name='toggle_follower'),
    re_path(r'^ajax/toggle/(?P<action>\w+)/(?P<param>\w+)/$', simple_toggle, name='simple_toggle'),
    re_path(r'^ajax/logout/$', LogoutView.as_view(), name="logout"),
    re_path(r'^ajax/action/model_edit/game/(?P<pk>\d+)/$', GameUpdateView.as_view(), name='update_game'),
    re_path(r'^ajax/action/model_edit/session/(?P<pk>\d+)/$', SessionUpdateView.as_view(), name='update_session'),
    re_path(r'^ajax/action/model_edit/profile/(?P<pk>\d+)/$', ProfileUpdateView.as_view(), name='update_profile'),
    re_path(r'^ajax/action/model_edit/campaign/(?P<pk>\d+)/$', CampaignUpdateView.as_view(), name='update_campaign'),
    re_path(r'^ajax/action/session_delete/(?P<pk>\d+)/$', delete_session, name='delete_session'),
    re_path(r'^ajax/action/session_campaign/(?P<pk>\d+)/$', delete_campaign, name='delete_campaign'),
    re_path(r'^register_submit/$', register_submit, name="register_submit"),
    re_path(r'^who/(?P<pk>\d+)/$', who, name="who"),

]
