from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from scheduler.models.realm import Realm
from colorfield.fields import ColorField

FACE_STYLES = (
    ('thin', '0'),
    ('standard', '1'),
    ('bold', '2')
)

HAIR_STYLES = (
    ('standard', '0'),
    ('type1', '1'),
    ('type2', '2'),
    ('type3', '3'),
    ('type4', '4'),
    ('type5', '5'),
    ('type6', '6'),
    ('type7', '7'),
    ('type8', '8'),
    ('type9', '9'),
    ('type10', '10'),
)

MOUTH_STYLES = (
    ('standard', '0'),
    ('type1', '1'),
    ('type2', '2'),
    ('type3', '3'),
    ('type4', '4'),
    ('type5', '5'),
    ('type6', '6'),
    ('type7', '7'),
    ('type8', '8'),
    ('type9', '9'),
    ('type10', '10')
)

ENGLISH_LEVEL = (
    ('0', 'No way!'),
    ('1', 'I can try'),
    ('2', 'Yes!'),
    ('3', "Okidoki. I can be gamemaster."),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=256)
    padid = models.CharField(max_length=4, default='', blank=True)
    presentation = models.TextField(max_length=2048, default='', blank=True)
    favorites = models.TextField(max_length=1024, default='', blank=True)
    club = models.CharField(max_length=256, default='', blank=True)
    need_drop = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    gaming_in_english = models.CharField(max_length=1, choices=ENGLISH_LEVEL, default='0')
    realm = models.ForeignKey(Realm, on_delete=models.SET_NULL, null=True, blank=True)
    is_girl = models.BooleanField(default=False)
    tracker_auto = models.BooleanField(default=False)
    face_style = models.CharField(max_length=256, default='standard', choices=FACE_STYLES)
    hair_style = models.CharField(max_length=256, default='standard', choices=HAIR_STYLES)
    mouth_style = models.CharField(max_length=256, default='standard', choices=MOUTH_STYLES)
    weeks = models.PositiveIntegerField(default=0, blank=True, null=True)
    alpha = ColorField(default='#666666')
    beta = ColorField(default='#666666')
    gamma = ColorField(default='#666666')
    hair = ColorField(default='#666666')
    eyes = ColorField(default='#666666')
    skin1 = ColorField(default='#CEB090')
    skin2 = ColorField(default='#9C8267')
    mail_wednesday = models.BooleanField(default=False)
    mail_sunday = models.BooleanField(default=False)
    mail_cyber_postit = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    override = models.CharField(max_length=256, default='{}', blank=True)

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

    def clean_track(self):
        from scheduler.models.follower import Follower
        all = Follower.objects.filter(profile=self).order_by('target__nickname')
        for x in all:
            x.delete()

    def auto_follow(self):
        from scheduler.models.session import Session
        import datetime
        sessions_as_mj = Session.objects.filter(mj=self, date_start__gt=datetime.now())  # todo
        sessions_where_wanted = Session.objects.filter(mj=self, date_start__gt=datetime.now())
        subscribed_sessions = Session.objects.filter(mj=self, date_start__gt=datetime.now())

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

    def update_portrait(self):
        if self.override != "{}":
            import json
            override = json.loads(self.override)
            self.face_style = override['face_style']
            self.hair_style = override['hair_style']
            self.mouth_style = override['mouth_style']
            self.override = '{}'

    def build_face_artefact(self):
        import json
        # Initialization
        mouth_styles_artefact = {}
        for item in MOUTH_STYLES:
            mouth_styles_artefact[item[0]] = 0.0
        face_styles_artefact = {}
        for item in FACE_STYLES:
            face_styles_artefact[item[0]] = 0.0
        hair_styles_artefact = {}
        for item in MOUTH_STYLES:
            hair_styles_artefact[item[0]] = 0.0
        artefact = {
            'face_style': face_styles_artefact,
            'hair_style': hair_styles_artefact,
            'mouth_style': mouth_styles_artefact
        }
        # Setting the values
        if self.override == "{}":
            artefact['face_style'][self.face_style] = 1.0
            artefact['hair_style'][self.hair_style] = 1.0
            artefact['mouth_style'][self.mouth_style] = 1.0
        else:
            override = json.loads(self.override)
            artefact['face_style'][override['face_style']] = 1.0
            artefact['hair_style'][override['hair_style']] = 1.0
            artefact['mouth_style'][override['mouth_style']] = 1.0
        return artefact

    def fetch_week_sessions(self):
        from datetime import date, timedelta
        from scheduler.models.session import Session
        from scheduler.views.gimme import gimme_session
        lists = {
            'sessions_where_mj': [],
            'sessions_where_wanted': [],
            'sessions_where_subscribed': [],
        }
        period_beginning = date.today()
        period_ending = date.today() + timedelta(days=28)
        sessions = Session.objects.filter(date_start__gte=period_beginning, date_start__lte=period_ending).order_by(
            'date_start')
        for s in sessions:
            subscribed = self.is_subscribed(s)
            wanted = self.is_wanted(s)
            mj = self.is_mj(s)
            if mj:
                lists['sessions_where_mj'].append(gimme_session(None, s))
            if wanted:
                lists['sessions_where_wanted'].append(gimme_session(None, s))
            if subscribed:
                lists['sessions_where_subscribed'].append(gimme_session(None, s))
        return lists

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
            required = self.is_wanted(s)
            if required:
                if not self.is_absent(s.date_start):

                    if len(inscription_set) == 0:
                        something_to_say = True
                        data.append(s)
                    else:
                        if s.id not in inscription_set:
                            something_to_say = True
                            data.append(s)
        return something_to_say, data

    def is_absent(self, d):
        from scheduler.models.availability import Availability
        result = False
        availabilities = Availability.objects.filter(profile=self, absent_mode=True, when=d)
        if len(availabilities) == 1:
            result = True
        return result

    def is_wanted(self, session=None):
        result = False
        if session:
            wanted = session.wanted.split(';')
            if len(wanted):
                if str(self.id) in wanted:
                    result = True
        return result

    def is_mj(self, session=None):
        result = False
        if session:
            if session.mj == self:
                result = True
        return result

    def is_subscribed(self, session=None):
        from scheduler.models.inscription import Inscription
        result = False
        if session:
            inscriptions = Inscription.objects.filter(session=session)
            for x in inscriptions:
                if self == x.profile:
                    result = True
        return result

    @property
    def get_portrait_codes(self):
        j = {
            'all': f'{self.get_face_style_display()}:{self.get_hair_style_display()}:{self.get_mouth_style_display()}',
            'face': self.get_face_style_display(),
            'hair': self.get_hair_style_display(),
            'mouth': self.get_mouth_style_display()
        }
        return j



class ProfileAdmin(admin.ModelAdmin):
    ordering = ['nickname']
    list_display = ['nickname', 'user', 'realm', 'games_run', 'presentation', 'favorites', 'mail_cyber_postit',
                    'mail_wednesday', 'mail_sunday', 'get_portrait_codes', 'override']
    list_filter = ['club']
