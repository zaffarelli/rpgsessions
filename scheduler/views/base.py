from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_TIME, FMT_DATE, FMT_DATETIME, DOWS, FMT_DATE_PRETTY
from scheduler.utils.organizer import build_month, build_zoomed_day, gimme_profile, system_flush, gimme_set_followers, \
    toggle_available, toggle_subscribe, gimme_session, gimme_profile_campaigns, gimme_profile_propositions, \
    gimme_campaign, gimme_all_propositions, gimme_profile_games
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
        template = get_template('scheduler/session_detail.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def display_campaign(request, id=None):
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
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_user(request, id)
    context['campaigns'] = gimme_profile_campaigns(id)
    context['propositions'] = gimme_profile_propositions(request,id)
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


def prepare_new_user(request, slug):
    from scheduler.models.realm import Realm
    context = {}
    realms = Realm.objects.all()
    realm = None
    for r in realms:
        if slug == r.invite_link:
            realm = r
    context['realm'] = realm.to_json
    return context


def handle_invitation(request, slug=None):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    context = prepare_new_user(request, slug)
    return render(request, 'registration/invite.html', context)


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
    context = {}
    form = SessionForm(request.POST or None, instance=session)
    if is_ajax(request):
        if form.is_valid():
            form.save()
        else:
            context['form'] = form
            context['session'] = gimme_session(request, session)
    return context


def gimme_edit_profile(request, profile):
    from scheduler.forms.profile_form import ProfileForm
    context = {}
    form = ProfileForm(request.POST or None, instance=profile)
    if is_ajax(request):
        if form.is_valid():
            form.save()
        else:
            context['form'] = form
            context['profile'] = gimme_profile(profile.id)
    return context


def gimme_edit_campaign(request, campaign):
    from scheduler.forms.campaign_form import CampaignForm
    context = {}
    form = CampaignForm(request.POST or None, instance=campaign)
    if is_ajax(request):
        if form.is_valid():
            form.save()
        else:
            context['form'] = form
            context['campaign'] = gimme_campaign(campaign.id)
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
    elif slug == "edit_profile":
        from scheduler.models.profile import Profile
        p = Profile.objects.get(pk=int(param))
        context = gimme_edit_profile(request, p)
        template_str = "scheduler/profile_edit_dialog.html"
    elif slug == "edit_campaign":
        from scheduler.models.campaign import Campaign
        c = Campaign.objects.get(pk=int(param))
        context = gimme_edit_campaign(request, c)
        template_str = "scheduler/campaign_edit_dialog.html"
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
    return context, template_str


# @login_required
def display_overlay(request, slug, param=None, option=None):
    html = ''
    callback = ''
    context, target_template = prepare_overlay(request, slug, param, option)
    # if is_ajax(request):
    #     print('Ajax Request')
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


def delete_campaign(request):
    pass


def register_submit(request):
    from django.contrib.auth.models import User
    from scheduler.models.profile import Profile
    from django.core.mail import send_mail
    valid = True
    errors = ['']
    is_girl = False
    html = ''
    if request.POST:
        username = request.POST['username'].replace(' ', '_').lower()
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        nickname = request.POST['nickname']
        if 'gender' in request.POST:
            is_girl = request.POST['gender'][0] == 'on'

        # Not an existing user
        if len(username) < 6:
            valid = False
            errors.append("Name too short")
        if len(nickname) < 3:
            valid = False
            errors.append("Nickname too short")
        all_users = User.objects.filter(username=username)
        if len(all_users):
            valid = False
            errors.append("User exists")
        if len(password) < 8:
            valid = False
            errors.append("Password too short")
        if password != confirm:
            valid = False
            errors.append("Password and confirm not equals")
        all_profiles = Profile.objects.filter(nickname=nickname)
        if len(all_profiles):
            valid = False
            errors.append("Profile already exists")
        if valid:
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            user.profile.nickname = nickname
            user.profile.is_girl = is_girl
            user.profile.save()
            host = request.get_host()
            send_mail('[eXtraventures] Enregistrement validé!',
                      f"Salut {nickname}...\nSi vous recevez cet email, c'est que votre enregistrement s'est bien passé.\n\n"
                      f"Votre login ................ {username}\n"
                      f"Votre mot de passe ......... {password}\n"
                      f"Le lien à eXtraventures .... https://{host}/\n"
                      f"\n\nVotre serviteur, Fernando Casabuentes",
                      f'fernando.casabuentes@gmail.com', [f'{email}'],
                      fail_silently=False)
            # send_mail(f'[eXtraventures] {nickname} Enregistrement validé!',
            #           f"Salut {nickname}...\nSi vous recevez cet email, c'est que votre enregistrement s'est bien passé.\n\n"
            #           f"Votre login ................ {username}\n"
            #           f"Le lien à eXtraventures .... https://{host}/\n"
            #           f"\n\nPour eXtraventures,\nVotre serviteur Fernando Casabuentes",
            #           f'fernando.casabuentes@gmail.com', [f'fernando.casabuentes@gmail.com'],
            #           fail_silently=False)
            html = "<center>Ok!! Surveillez vos messages,<BR/>vous recevrez la suite par email.</center>"
        else:
            send_mail("[eXtraventures] Erreur d'enregistrement!",
                      f'Failed attempt..\n\n{request.POST}\n\n{errors}',
                      f'fernando.casabuentes@gmail.com', [f'zaffarelli@gmail.com'], fail_silently=False)

            html = f"<center>Oups!! Il y a eu quelques problèmes.. {'<BR/>- '.join(errors)}<br><br>Merci de réessayer.</center>"
    response = {'data': html}
    return JsonResponse(response)


@login_required
def propositions(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = {}
    context['today'] = datetime.now().strftime(FMT_DATE)
    context['propositions'] = gimme_all_propositions(request,request.user.profile.id)
    template = get_template('scheduler/menu_propositions.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/all_propositions.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)
