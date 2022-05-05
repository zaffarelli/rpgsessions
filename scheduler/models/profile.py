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
    ('crystal', 'Cristal'),
)

FACE_STYLES = (
    ('thin', 'Mince'),
    ('standard', 'Moyen'),
    ('bold', 'Large')
)

HAIR_STYLES = (
    ('standard', 'Sans'),
    ('type1', 'Cheveux 1'),
    ('type2', 'Cheveux 2'),
    ('type3', 'Cheveux 3'),
    ('type4', 'Cheveux 4'),
    ('type5', 'Cheveux 5'),
    ('type6', 'Cheveux 6')
)

MOUTH_STYLES = (
    ('standard', 'Sans'),
    ('type1', 'Type 1'),
    ('type2', 'Type 2'),
    ('type3', 'Type 3'),
    ('type4', 'Type 4'),
    ('type5', 'Type 5'),
    ('type6', 'Type 6')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    favorites = models.TextField(max_length=1024, default='', blank=True)
    club = models.CharField(max_length=256, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True, blank=True)
    is_girl = models.BooleanField(default=False)
    # shield = models.CharField(max_length=256, default='shield_base')
    # silhouette = models.CharField(max_length=256, default='player_base')
    # shieldstyle = models.CharField(max_length=256, default='mid', choices=SHIELD_STYLES)
    # iconstyle = models.CharField(max_length=256, default='disk', choices=ICON_STYLES)
    face_style = models.CharField(max_length=256, default='standard', choices=FACE_STYLES)
    hair_style = models.CharField(max_length=256, default='standard', choices=HAIR_STYLES)
    mouth_style = models.CharField(max_length=256, default='standard', choices=MOUTH_STYLES)
    # svg_artefact = models.CharField(max_length=256, default='{}')
    weeks = models.PositiveIntegerField(default=0, blank=True, null=True)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')
    hair = ColorField(default='#666666')
    eyes = ColorField(default='#666666')
    mail_wednesday = models.BooleanField(default=False)
    mail_sunday = models.BooleanField(default=False)
    mail_cyber_postit = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

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
        from scheduler.views.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(profile=self).order_by('target__nickname')
        for x in all:
            list.append(gimme_profile(x.target.id))
        return list

    @property
    def groupies(self):
        from scheduler.models.follower import Follower
        from scheduler.views.organizer import gimme_profile
        list = []
        all = Follower.objects.filter(target=self).order_by('profile__nickname')
        for x in all:
            list.append(gimme_profile(x.profile.id))
        return list

    @property
    def games_run(self):
        from scheduler.models.session import Session
        from datetime import date
        all = Session.objects.filter(mj=self, date_start__lt=date.today())
        return len(all)

    @property
    def games_played(self):
        from scheduler.models.inscription import Inscription
        all = Inscription.objects.filter(profile=self)
        return len(all)

    # @property
    # def silhouette_symbol(self):
    #     girl = ''
    #     if self.is_girl:
    #         girl = ''
    #     return f"scheduler/svg/{self.silhouette}{girl}.svg"
    #
    # @property
    # def shield_symbol(self):
    #     return f"scheduler/svg/{self.shield}.svg"

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

    # def build_svg_artefact(self):
    #     artefact = {
    #         'shield_back': {
    #             'mid': 0.0,
    #             'half': 0.0,
    #             'quad': 0.0
    #         },
    #         'icon': {
    #             'disk': 0.0,
    #             'coins': 0.0,
    #             'cross': 0.0,
    #             'claws': 0.0,
    #             'diamond': 0.0,
    #             'crystal': 0.0,
    #         }
    #     }
    #     artefact['shield_back'][self.shieldstyle] = 1.0
    #     artefact['icon'][self.iconstyle] = 1.0
    #     return artefact

    def build_face_artefact(self):
        artefact = {
            'face_style': {
                'thin': 0.0,
                'standard': 0.0,
                'bold': 0.0
            },
            'hair_style': {
                'standard': 0.0,
                'type1': 0.0,
                'type2': 0.0,
                'type3': 0.0,
                'type4': 0.0,
                'type5': 0.0,
                'type6': 0.0

            },
            'mouth_style': {
                'standard': 0.0,
                'type1': 0.0,
                'type2': 0.0,
                'type3': 0.0,
                'type4': 0.0,
                'type5': 0.0,
                'type6': 0.0
            }
        }
        artefact['face_style'][self.face_style] = 1.0
        artefact['hair_style'][self.hair_style] = 1.0
        artefact['mouth_style'][self.mouth_style] = 1.0
        return artefact

    def fetch_week_sessions(self):
        from datetime import date, timedelta
        from scheduler.models.session import Session
        list = []
        period_beginning = date.today()
        period_ending = date.today() + timedelta(days=7)
        sessions = Session.objects.filter(date_start__gte=period_beginning, date_start__lt=period_ending).order_by(
            'date_start')
        for s in sessions:
            list.append(f"{s.date_start} - '{s.title}' par {s.mj}")
        return list

    def played_the(self, d, de):
        """ Check if the profile has inscriptions on sessions between d and de included """
        from scheduler.models.session import Session
        from scheduler.models.inscription import Inscription
        inscriptions = Inscription.objects.filter(profile=self)
        inscription_set = []
        for i in inscriptions:
            if i.session.date_start:
                if d <= i.session.date_start and i.session.date_start <= de:
                    inscription_set.append(i.session.id)
        sessions = Session.objects.filter(date_start__gte=d, date_start__lte=de)
        data = []
        something_to_say = False
        for s in sessions:
            # required = self.id in s.wanted.split(';')
            if s.id in inscription_set:
                something_to_say = True
                data.append(s)
        return something_to_say, data

    def masterized_the(self, d, de):
        """ Check if the profile is mj on sessions between d and de included """
        from scheduler.models.session import Session
        sessions_mj = Session.objects.filter(date_start__gte=d, date_start__lte=de, mj=self)
        something_to_say = len(sessions_mj) > 0
        data = []
        for s in sessions_mj:
            data.append(s)
        return something_to_say, data

    def wanted_the(self, d, de):
        """ Check if the profile has inscriptions on sessions between d and de included """
        from scheduler.models.session import Session
        from scheduler.models.inscription import Inscription
        inscriptions = Inscription.objects.filter(profile=self)
        inscription_set = []
        for i in inscriptions:
            if i.session.date_start:
                if d <= i.session.date_start and i.session.date_start <= de:
                    inscription_set.append(i.session.id)
        sessions = Session.objects.filter(date_start__gte=d, date_start__lte=de)
        data = []
        something_to_say = False
        for s in sessions:
            required = self.id in s.wanted.split(';')
            if required:
                if s.id not in inscription_set:
                    something_to_say = True
                    data.append(s)
        return something_to_say, data


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['nickname', 'user', 'realm', 'games_run', 'presentation', 'favorites', 'mail_cyber_postit',
                    'mail_wednesday', 'mail_sunday']
    list_filter = ['club']
