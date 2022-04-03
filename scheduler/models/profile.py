from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from scheduler.models.realm import Realm
from colorfield.fields import ColorField

SHIELD_STYLES = (
    ('mid', 'Gauche et droite'),
    ('quad', 'Quadrants NO, NE, SE, SW en damier'),
    ('half', 'Haut et bas séparés'),
)

ICON_STYLES = (
    ('disk', 'Disque'),
    ('coins', 'Trois deniers'),
    ('cross', 'Croix'),
    ('claws', 'Griffure'),
    ('diamond', 'Losange'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    favorites = models.TextField(max_length=1024, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True)
    is_girl = models.BooleanField(default=False)
    shield = models.CharField(max_length=256, default='shield_base')
    silhouette = models.CharField(max_length=256, default='player')
    shield_style = models.CharField(max_length=256, default='mid', choices=SHIELD_STYLES)
    icon_style = models.CharField(max_length=256, default='disk', choices=ICON_STYLES)
    svg_artefact = models.CharField(max_length=256, default='{}')
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')

    def __str__(self):
        return f'{self.nickname}*'

    @property
    def u_u(self):
        return self.user.username

    @property
    def to_json(self):
        from scheduler.utils.mechanics import json_default
        import json
        return json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))

    @property
    def following(self):
        from scheduler.models.follower import Follower
        from scheduler.utils.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(profile=self).order_by('target__nickname')
        for x in all:
            list.append(gimme_profile(x.target.id))
        return list

    @property
    def groupies(self):
        from scheduler.models.follower import Follower
        from scheduler.utils.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(target=self).order_by('profile__nickname')
        for x in all:
            list.append(gimme_profile(x.profile.id))
        return list

    @property
    def games_run(self):
        from scheduler.models.session import Session
        all = Session.objects.filter(mj=self)
        return len(all)

    @property
    def silhouette_symbol(self):
        girl = ''
        if self.is_girl:
            girl = '_girl'
        return f"scheduler/svg/{self.silhouette}{girl}.svg"

    @property
    def shield_symbol(self):
        return f"scheduler/svg/{self.shield}.svg"

    def send_pwd_reset_mail(self):
        from django.core.mail import send_mail
        send_mail(
            '[eXtraventures] Réinitialisation de mot de passe.',
            'Vous avez demandé une réinitialisation de mot de passe. Merci de suivre ce <a href="">lien<a>',
            'augustus.pepermint@gmail.com',
            [self.email],
            fail_silently=True,
        )
        return

    def build_svg_artefact(self):
        artefact = {
            'shield_back': {
                'mid': 0.0,
                'half': 0.0,
                'quad': 0.0
            },
            'icon': {
                'disk': 0.0,
                'coins': 0.0,
                'cross': 0.0,
                'claws': 0.0,
                'diamond': 0.0,
            }
        }
        artefact['shield_back'][self.shield_style] = 1.0
        artefact['icon'][self.icon_style] = 1.0
        return artefact


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['u_u', 'nickname', 'realm', 'games_run', 'shield', 'silhouette', 'presentation', 'favorites']
