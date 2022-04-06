from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_TIME, FMT_DATE, FMT_DATETIME, DOWS, FMT_DATE_PRETTY
from scheduler.utils.organizer import build_month, build_zoomed_day, gimme_profile, system_flush, gimme_set_followers, \
    toggle_available, toggle_subscribe, gimme_session
from datetime import datetime, date
from scheduler.utils.tools import is_ajax


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
        template = get_template('scheduler/session_detail_old.html')
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


def gimme_new_session(request, param):
    from scheduler.models.session import Session
    s = Session()
    s.title = f'Partie créée le {datetime.now()} par {request.user.profile.nickname}'
    s.mj = request.user.profile
    s.date_start = date.fromisoformat(param.replace('_', '-'))
    s.save()
    context = {'session': s}
    return context


def gimme_edit_session(request, session):
    from scheduler.forms.session_form import SessionForm
    # from scheduler.models.session import Session
    context = {}
    form = SessionForm(request.POST or None, instance=session)
    if is_ajax(request):
        print('is ajax in gimme_edit_session')
        if form.is_valid():
            print("The form is valid")
            form.save()
        else:
            print("The form is NOT valid")
            context['form'] = form
            context['session'] = gimme_session(request, session)
    # context['date'] = form.fields['date_start'].value #strftime(FMT_DATE)
    return context


def prepare_overlay(request, slug, param=None, option=None):
    context = {}
    template_str = ""
    if slug == "new_session":
        context = gimme_new_session(request, param)
        template_str = "scheduler/session_create_dialog.html"
    elif slug == "edit_session":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        context = gimme_edit_session(request, s)
        template_str = "scheduler/session_edit_dialog.html"
    # elif slug == "update_session":
    #     from scheduler.models.session import Session
    #     s = Session.objects.get(pk=int(param))
    #     context = gimme_edit_session(request, s)
    #     template_str = "scheduler/session_edit_dialog.html"
    elif slug == "delete_session":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        context = {'session': gimme_session(request, s)}
        template_str = "scheduler/session_delete_dialog.html"
    elif slug == "about":
        template_str = "scheduler/about.html"
    elif slug == "followers":
        context["set_followers"] = gimme_set_followers(request.user.profile.id)
        template_str = "scheduler/set_followers.html"
    elif slug == "confirm":
        from scheduler.models.session import Session
        s = Session.objects.get(pk=int(param))
        s.delete()

    return context, template_str




# @login_required
def display_overlay(request, slug, param=None, option=None):
    html = ''
    callback = ''
    context, target_template = prepare_overlay(request, slug, param, option)
    if is_ajax(request):
        print('Ajax Request')
    if target_template:
        template = get_template(target_template)
        html = template.render(context, request)
    response = {'data': html, 'callback': callback}
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
