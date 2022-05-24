from scheduler.models.session import Session
from scheduler.models.game import Game
from scheduler.models.profile import FACE_STYLES, HAIR_STYLES, MOUTH_STYLES, Profile
from django.contrib.auth.models import User
import random
import datetime


class Populate(object):
    def remove_sessions(self):
        for session in Session.objects.all():
            session.delete()

    def remove_profiles(self):
        for user in User.objects.exclude(username='zaffarelli'):
            user.delete()

    def clean_up(self):
        """ Remove all games """
        self.remove_sessions()
        self.remove_profiles()

    def randcol(self):
        r = lambda: random.randint(0, 255)
        return f'#{r():02X}{r():02X}{r():02X}'

    def add_users(self):
        """ Add games in the upcoming month """
        EYES = ['#1D2C38', '#26B4E6', '#496744', '#522E12', '#2B2119', '#9D9D58']
        HAIRS = ['#E5A75B', '#2C1A04', '#E1B640', '#120E02', '#302119', '#46514F']



        set_of_users = [
            {'name': 'john', 'is_girl': False},
            {'name': 'jody', 'is_girl': True},
            {'name': 'steven', 'is_girl': False},
            {'name': 'billie', 'is_girl': True},
            {'name': 'zach', 'is_girl': False},
            {'name': 'lou', 'is_girl': True},
            {'name': 'rick', 'is_girl': False},
            {'name': 'seb', 'is_girl': False},
            {'name': 'thomas', 'is_girl': False},
            {'name': 'scott', 'is_girl': False},
            {'name': 'vic', 'is_girl': False},
            {'name': 'karl', 'is_girl': False},
            {'name': 'sondra', 'is_girl': True},
            {'name': 'nico', 'is_girl': False},
            {'name': 'jordan', 'is_girl': False},
            {'name': 'ryan', 'is_girl': False}
        ]
        for u in set_of_users:
            x = User()
            x.username = u['name']
            x.set_password(u['name'])
            x.email = 'fernando.casabuentes@gmail.com'
            x.save()
            p = x.profile
            p.is_girl = u['is_girl']
            p.nickname = u['name'].title()
            p.alpha = self.randcol()
            p.beta = self.randcol()
            p.gamma = self.randcol()
            p.face_style = random.choice(FACE_STYLES)[0]
            p.mouth_style = random.choice(MOUTH_STYLES)[0]
            p.hair_style = random.choice(HAIR_STYLES)[0]
            p.eyes = random.choice(EYES)
            p.hair = random.choice(HAIRS)
            p.club = random.choice(['Extraventures', 'Voleurs de Bonnefoy', 'Supelec', "Rue d'Ulm", '', ''])
            p.can_drop = random.choice([False, False, True])
            p.need_drop = random.choice([True, False, False])
            p.save()

    def add_sessions(self):
        """ Add games in the upcoming month """
        all_games = Game.objects.exclude(name='Autre')
        all_players = Profile.objects.all()
        phonems = ["lo", "ca", "ci", "ta", "oc", "om", "on", "di", "da", "al", "zu", "ri", "ro"]
        for x in range(10):
            s = Session()
            if x < 5:
                s.mj = Profile.objects.get(nickname='zaffarelli')
            else:
                s.mj = random.choice(all_players)
            s.game = random.choice(all_games)
            a = datetime.date.today() + datetime.timedelta(days=random.randint(1, 5))
            b = datetime.date.today() + datetime.timedelta(days=random.randint(1, 10))
            c = datetime.date.today() + datetime.timedelta(days=random.randint(1, 15))
            s.date_start = random.choice([None, a, b, c, a,b,c])
            s.alpha = s.game.alpha
            s.place = f"chez {s.mj.nickname}"
            s.title = "".join(random.choices(phonems,k=4)).title()
            wanted = random.choices(population=all_players, k=random.randint(3, 7))
            print("wanted", wanted)
            if s.mj.id in wanted:
                wanted.remove(s.mj)
            print(wanted)
            wanted = list(set(wanted))
            print(wanted)
            wanted_ids = []
            for x in wanted:
                wanted_ids.append(str(x.id))
            print("wanted_ids", wanted_ids)
            s.wanted = ";".join(wanted_ids)
            print(s.wanted)
            s.is_visible = True
            s.save()

    def perform(self):
        self.clean_up()
        self.add_users()
        self.add_sessions()


Populate().perform()