from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_DATE, DOWS, FMT_DATE_PRETTY
from scheduler.views.organizer import build_month, toggle_available, toggle_subscribe, prepare_day, prepare_month
from scheduler.views.gimme import gimme_profile, gimme_set_followers
from scheduler.views.misc import system_flush
from datetime import datetime


def prepare_index(request):
    d = datetime.now()
    m = build_month(request, d.strftime(FMT_DATE))
    u = gimme_profile(request.user.profile.id)
    context = {'fontset': FONTSET, 'month': m, 'u': u}
    return context


@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    system_flush()
    context = prepare_index(request)
    return render(request, 'scheduler/index.html', context=context)


@login_required
def display_day(request, slug=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_day(request, slug)
    template = get_template('scheduler/menu_dayzoom.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/day_zoom.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


@login_required
def display_month(request, slug=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_month(request, slug)
    template = get_template('scheduler/menu_month.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/month.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


@login_required
def display_session(request, id=None):
    from scheduler.views.organizer import prepare_session
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_session(request, id)
    html = 'WTF?'
    menu_html = 'WTF?'
    if context['status'] == 'OK':
        template = get_template('scheduler/menu_session.html')
        menu_html = template.render(context, request)
        template = get_template('scheduler/session_detail.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def display_campaign(request, id=None):
    return JsonResponse({})


def display_game(request, id=None):
    return JsonResponse({})


def prepare_user(request, id=None):
    from scheduler.models.profile import Profile
    all = Profile.objects.filter(pk=id)
    cur_date = datetime.now()
    context = {'status': 'KO'}
    if len(all) == 1:
        context['status'] = 'OK'
        that = all.first()
        context['profile'] = gimme_profile(that.id)

    day_off = cur_date.weekday() > 4
    current_day = cur_date.day == datetime.today().day
    day = {'date': cur_date,
           'day_off': day_off,
           'current_day': current_day,
           'day': cur_date.strftime(FMT_DATE),
           'day_info': f'{DOWS[cur_date.weekday()]}<BR/><small>{cur_date.strftime(FMT_DATE_PRETTY)}</small>'
           }
    context['day'] = day
    return context


@login_required
def display_user(request, id=None):
    from scheduler.views.gimme import gimme_profile_campaigns, gimme_profile_propositions, gimme_profile_games
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_user(request, id)
    context['campaigns'] = gimme_profile_campaigns(id)
    context['propositions'] = gimme_profile_propositions(request, id)
    context['games'] = gimme_profile_games(id)
    context['realm'] = request.user.profile.realm.to_json
    html = 'WTF?'
    menu_html = 'WTF?'
    if context['status'] == 'OK':
        template = get_template('scheduler/menu_user.html')
        menu_html = template.render(context, request)
        template = get_template('scheduler/user_details.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


@login_required
def toggle_follower(request, id):
    from scheduler.models.follower import Follower
    from scheduler.models.profile import Profile
    # print("+++ HERE +++", id)
    profile = Profile.objects.get(pk=request.user.profile.id)
    target = Profile.objects.get(pk=id)
    context = {}
    html = ''
    all = Follower.objects.filter(profile=profile, target=target)
    if len(all) == 1:
        all.first().delete()
    else:
        x = Follower(profile=profile, target=target)
        x.save()
        # html = gimme_profile(target.id)
    context["set_followers"] = gimme_set_followers(request.user.profile.id)
    template = get_template("scheduler/set_followers.html")
    html = template.render(context, request)
    response = {'data': html}
    return JsonResponse(response)


@login_required
def simple_toggle(request, action, param):
    if action in ['set_absent', 'set_available']:
        html, target = toggle_available(request, action, param)
    elif action in ['session_subscribe']:
        html, target = toggle_subscribe(request, action, param)
    response = {'data': html, 'target': target}
    return JsonResponse(response)


def show_done(request, pk=None):
    return render(request, 'scheduler/done.html')


def delete_session(request):
    pass


def delete_campaign(request):
    pass


def validate_game(request, pk=None):
    from scheduler.forms.game_form import GameForm
    from scheduler.models.game import Game
    from scheduler.views.gimme import gimme_game
    response = {'form': '', 'data': '', 'callback': '', 'game_id': pk}
    g = Game.objects.get(pk=int(pk))
    form = GameForm(request.POST or None, instance=g)
    if form.is_valid():
        form.save()
        g = Game.objects.get(pk=int(pk))
        ctx = {'c': gimme_game(g)}
        template = get_template("scheduler/game_row.html")
        response['callback'] = template.render(ctx, request)
        response['form'] = "Okidoki!"
    else:
        response['form'] = form
    return JsonResponse(response)


def validate_profile(request, pk=None):
    from scheduler.forms.profile_form import ProfileForm
    from scheduler.models.profile import Profile
    response = {'form': '', 'data': '', 'callback': '', 'profile_id': pk}
    p = Profile.objects.get(pk=int(pk))
    form = ProfileForm(request.POST or None, instance=p)
    if form.is_valid():
        form.save()
        p = Profile.objects.get(pk=int(pk))
        ctx = {'profile': gimme_profile(p.id)}
        template = get_template("scheduler/profile_details.html")
        response['callback'] = template.render(ctx, request)
        response['form'] = "Okidoki!"
    else:
        response['form'] = form
    return JsonResponse(response)


def validate_session(request, pk=None):
    from scheduler.forms.session_form import SessionForm
    from scheduler.models.session import Session
    from scheduler.views.gimme import gimme_session
    response = {'form': '', 'data': '', 'callback': '', 'session_id': pk}
    s = Session.objects.get(pk=int(pk))
    form = SessionForm(request.POST or None, instance=s)
    if form.is_valid():
        form.save()
        s = Session.objects.get(pk=int(pk))
        ctx = {'c': gimme_session(request, s)}
        template = get_template("scheduler/proposition_row.html")
        response['callback'] = template.render(ctx, request)
        response['form'] = "Okidoki!"
    else:
        response['form'] = form
    return JsonResponse(response)


def validate_campaign(request, pk=None):
    from scheduler.forms.campaign_form import CampaignForm
    from scheduler.models.campaign import Campaign
    from scheduler.views.gimme import gimme_campaign
    response = {'form': '', 'data': '', 'callback': '', 'campaign_id': pk}
    c = Campaign.objects.get(pk=int(pk))
    form = CampaignForm(request.POST or None, instance=c)
    if form.is_valid():
        form.save()
        c = Campaign.objects.get(pk=int(pk))
        ctx = {'c': gimme_campaign(c.id)}
        template = get_template("scheduler/campaign_row.html")
        response['callback'] = template.render(ctx, request)
        response['form'] = "Okidoki!"
    else:
        response['form'] = form
    return JsonResponse(response)


def gimme_edit_campaign(campaign):
    from scheduler.forms.campaign_form import CampaignForm
    response = {'form': '', 'data': '', 'callback': '', 'campaign_id': campaign.id}
    form = CampaignForm(instance=campaign)
    response['form'] = form
    return response


def gimme_edit_session(session):
    from scheduler.forms.session_form import SessionForm
    response = {'form': '', 'data': '', 'callback': '', 'session_id': session.id}
    form = SessionForm(instance=session)
    response['form'] = form
    return response


def gimme_edit_profile(profile):
    from scheduler.forms.profile_form import ProfileForm
    response = {'form': '', 'data': '', 'callback': '', 'profile_id': profile.id}
    form = ProfileForm(instance=profile)
    response['form'] = form
    return response


def gimme_edit_game(game):
    from scheduler.forms.game_form import GameForm
    response = {'form': '', 'data': '', 'callback': '', 'game_id': game.id}
    form = GameForm(instance=game)
    response['form'] = form
    return response


def prepare_overlay(request, slug, param=None, option=None):
    from scheduler.views.gimme import gimme_new_session, gimme_new_campaign, gimme_session, gimme_campaign, gimme_set_followers
    context = {}
    more = {}
    template_str = ""
    if slug == "new_session":
        context = gimme_new_session(request, param)
        template_str = "scheduler/session_create_dialog.html"
    elif slug == "new_campaign":
        context = gimme_new_campaign(request, param)
        template_str = "scheduler/campaign_create_dialog.html"
    elif slug == "edit_session":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        context = gimme_edit_session(s)
        template_str = "scheduler/session_edit_dialog.html"
    elif slug == "edit_profile":
        from scheduler.models.profile import Profile
        p = Profile.objects.get(pk=int(param))
        context = gimme_edit_profile(p)
        template_str = "scheduler/profile_edit_dialog.html"
    elif slug == "edit_campaign":
        from scheduler.models.campaign import Campaign
        c = Campaign.objects.get(pk=int(param))
        context = gimme_edit_campaign(c)
        template_str = "scheduler/campaign_edit_dialog.html"
    elif slug == "edit_game":
        from scheduler.models.game import Game
        g = Game.objects.get(pk=int(param))
        context = gimme_edit_game(g)
        template_str = "scheduler/game_edit_dialog.html"
    elif slug == "delete_session":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        context = {'session': gimme_session(request, s)}
        template_str = "scheduler/session_delete_dialog.html"
    elif slug == "delete_campaign":
        from scheduler.models.campaign import Campaign
        c = Campaign.objects.get(pk=int(param))
        context = {'campaign': gimme_campaign(c.id)}
        template_str = "scheduler/campaign_delete_dialog.html"
    elif slug == "about":
        template_str = "scheduler/about.html"
    elif slug == "followers":
        context["set_followers"] = gimme_set_followers(request.user.profile.id)
        template_str = "scheduler/set_followers.html"
    elif slug == "confirm_session":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        s.delete()
    elif slug == "confirm_campaign":
        from scheduler.models.campaign import Campaign
        c = Campaign.objects.get(pk=int(param))
        c.delete()
    return context, template_str, more


# @login_required
def display_overlay(request, slug, param=None, option=None):
    html = ''
    context, target_template, callback = prepare_overlay(request, slug, param, option)
    if target_template:
        template = get_template(target_template)
        html = template.render(context, request)
    response = {'data': html, 'callback': callback}
    return JsonResponse(response)
