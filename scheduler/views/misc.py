from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scheduler.utils.mechanics import FONTSET, random_color
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime


def prepare_who(request, pk):
    from scheduler.views.gimme import gimme_profile
    u = gimme_profile(pk)
    context = {'fontset': FONTSET, 'u': u}
    return context


@login_required
def who(request, pk=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    if pk is None:
        pk = 1
    context = prepare_who(request, pk)
    return render(request, 'scheduler/who.html', context=context)


def register_submit(request):
    from django.contrib.auth.models import User
    from scheduler.models.profile import Profile
    from django.core.mail import send_mail
    from scheduler.models.follower import Follower
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
            errors.append("Nom top court (6 cracatères mini)")
        purged = username.replace(" ", "").replace("<", "").replace("-", "").replace("&", "").replace("!", "").replace(
            "?", "").replace("/", "")
        if purged != username:
            valid = False
            errors.append("Caractères invalides dans l'identifiant...")

        if len(nickname) < 3:
            valid = False
            errors.append("Surnom trop court")
        all_users = User.objects.filter(username=username)
        if len(all_users):
            valid = False
            errors.append("Cet utilisateur existe déjà...")
        if len(password) < 8:
            valid = False
            errors.append("Mot de passe trop court")
        if password != confirm:
            valid = False
            errors.append("Le mot de passe et la confirmation ne correspondent pas...")
        all_profiles = Profile.objects.filter(nickname=nickname)
        if len(all_profiles):
            valid = False
            errors.append("Ce profil existe déjà...")
        if valid:
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            user.profile.nickname = nickname
            user.profile.is_girl = is_girl
            user.profile.mail_cyber_postit = True
            user.profile.alpha = random_color()
            user.profile.beta = random_color()
            user.profile.gamma = random_color()
            user.profile.save()
            # Auto follow self at first
            f = Follower()
            f.profile = user.profile
            f.target = user.profile
            f.save()
            host = request.get_host()
            send_mail('[eXtraventures] Enregistrement validé!',
                      f"Salut {nickname}...\nSi vous recevez cet email, c'est que votre enregistrement s'est bien passé.\n\n"
                      f"Votre login ................ {username}\n"
                      f"Votre mot de passe ......... {password}\n"
                      f"Le lien à eXtraventures .... https://{host}/\n"
                      f"\n\nVotre serviteur, Fernando Casabuentes",
                      f'fernando.casabuentes@gmail.com', [f'{email}'],
                      fail_silently=False)
            html = "<center>Ok!! Surveillez vos messages,<BR/>vous recevrez la suite par email.</center>"
        else:
            send_mail("[eXtraventures] Erreur d'enregistrement!",
                      f'Failed attempt..\n\n{request.POST}\n\n{errors}',
                      f'fernando.casabuentes@gmail.com', [f'zaffarelli@gmail.com', email], fail_silently=False)

            html = f"<center>Oups!! Il y a eu quelques problèmes.. {'<BR/>- '.join(errors)}<br><br>Merci de réessayer.</center>"
    response = {'data': html}
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


def prepare_design(request):
    from scheduler.models.profile import Profile
    from scheduler.models.profile import HAIR_STYLES, MOUTH_STYLES, FACE_STYLES
    from scheduler.views.gimme import gimme_profile_sober

    p = Profile()
    p.alpha = "#ff0000"
    p.beta = "#00ff00"
    p.gamma = "#0000ff"
    p.face_style = "standard"
    p.hair_style = "standard"
    p.mouth_style = "standard"
    p.is_girl = False
    p.hair = "#ffff00"
    p.eyes = "#00ffff"
    p.skin1 = "#cc00cc"
    p.skin2 = "#880088"

    hair = []
    mouth = []
    face = []

    for i in HAIR_STYLES:
        p.is_girl = False
        p.hair_style = i[0]
        hair.append(gimme_profile_sober(p))
        p.is_girl = True
        hair.append(gimme_profile_sober(p))
    p.hair_style = "standard"
    for i in MOUTH_STYLES:
        p.is_girl = False
        p.mouth_style = i[0]
        mouth.append(gimme_profile_sober(p))
        p.is_girl = True
        mouth.append(gimme_profile_sober(p))
    p.mouth_style = "standard"
    for i in FACE_STYLES:
        p.is_girl = False
        p.face_style = i[0]
        face.append(gimme_profile_sober(p))
        p.is_girl = True
        face.append(gimme_profile_sober(p))
    context = {'figures': {'hair': hair, 'mouth': mouth, 'face': face}}
    return context


@login_required
def design(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_design(request)
    return render(request, 'scheduler/design.html', context=context)


def system_flush():
    from scheduler.models.availability import Availability
    # Suppression des disponibilités antérieures à la date du jour
    data_from_the_past = Availability.objects.filter(when__lt=datetime.today())
    for i in data_from_the_past:
        i.delete()
    # from scheduler.models.inscription import Inscription
