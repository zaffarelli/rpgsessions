from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_TIME, FMT_DATE, FMT_DATETIME, DOWS, FMT_DATE_PRETTY
from scheduler.utils.organizer import build_month, build_zoomed_day, gimme_profile
from datetime import datetime, date


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
    context = prepare_index(request)
    print(context)
    return render(request, 'scheduler/index.html', context=context)


def prepare_day(request, slug=None):
    slug = slug.replace('_', '-')
    d = date.fromisoformat(slug)
    data = build_zoomed_day(request, d)
    context = {'data': data}
    return context


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


def prepare_month(request, slug=None):
    if slug is None:
        d = datetime.now()
    else:
        slug = slug.replace("_", "-")
        d = date.fromisoformat(slug)
    m = build_month(request, d.strftime(FMT_DATE))
    context = {'c': m}
    return context


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


def prepare_session(request, id=None):
    from scheduler.models.session import Session
    from scheduler.models.profile import Profile
    from scheduler.utils.organizer import gimme_profile, gimme_session, gimme_day, gimme_all_availabilities
    all = Session.objects.filter(pk=id)
    cur_date = datetime.now()
    context = {'status': 'KO'}
    if len(all) == 1:
        context['status'] = 'OK'
        that = all.first()
        inscriptions = []
        for i in that.inscription_set.all().order_by('profile__user_id'):
            inscriptions.append(gimme_profile(i.profile.id))
        context['session'] = gimme_session(request, that)
        context['game'] = that.game.to_json
        context['mj'] = gimme_profile(that.mj.id)
        context['owner'] = that.mj.user == request.user
        context['wanted_list'] = that.wanted_list
        context['inscriptions'] = inscriptions
        context['availabilities'] = gimme_all_availabilities(request, cur_date, request.user.profile.id)
    context['day'] = gimme_day(request, cur_date)
    return context


@login_required
def display_session(request, id=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_session(request, id)
    html = 'WTF?'
    menu_html = 'WTF?'
    if context['status'] == 'OK':
        template = get_template('scheduler/menu_session.html')
        menu_html = template.render(context, request)
        template = get_template('scheduler/session_details.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def prepare_user(request, id=None):
    from scheduler.models.profile import Profile
    all = Profile.objects.filter(pk=id)
    cur_date = datetime.now()
    context = {'status': 'KO'}
    if len(all) == 1:
        context['status'] = 'OK'
        that = all.first()
        context['profile'] = that.to_json

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
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_user(request, id)
    html = 'WTF?'
    menu_html = 'WTF?'
    if context['status'] == 'OK':
        template = get_template('scheduler/menu_user.html')
        menu_html = template.render(context, request)
        template = get_template('scheduler/user_details.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def new_user(request, slug):
    return {}


def handle_invitation(request, slug=None):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    context = prepare_new(request, slug)
    template = get_template('registration/invite.html')
    html = template.render(context, request)
    response = {'data': html}
    return JsonResponse(response)
