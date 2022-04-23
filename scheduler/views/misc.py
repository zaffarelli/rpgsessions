from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scheduler.utils.mechanics import FONTSET

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


def system_flush():
    from scheduler.models.availability import Availability
    data_from_the_past = Availability.objects.filter(when__lt=datetime.today())
    for i in data_from_the_past:
        i.delete()
    # from scheduler.models.inscription import Inscription

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