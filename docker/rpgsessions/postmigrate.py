# To be run once

from scheduler.models.realm import Realm
from scheduler.models.game import Game

for r in Realm.objects.all():
    r.delete()

for g in Game.objects.all():
    g.delete()

realm = Realm()
realm.name = 'JDR31'
realm.key = '%JDR$$31%'
realm.description = 'Ceci est le domaine de la communauté JDR 31.'
realm.save()

GAMES = [
    {'name': 'Fading Suns',
     'version': 'Fuzion Interlock Custom System',
     'acronym': 'FS',
     'description': "A l'aube du sixième millénaire, l'humanité s'est perdue aux confins du cosmos. ",
     "alpha": "#CCCCCC",
     "beta": "#888888",
     "gamma": "#FFCC44"
     },
    {'name': 'Dungeons & Dragons',
     'version': '5ème Edition',
     'acronym': 'D&D5',
     'description': "",
     "alpha": "#222222",
     "beta": "#AA2020",
     "gamma": "#222222"
     },
    {'name': 'Dungeons & Dragons',
     'version': '3.5 Edition',
     'acronym': 'D&D3.5',
     'description': "",
     "alpha": "#112233",
     "beta": "#AA2020",
     "gamma": "#222222"
     },
]

for g in GAMES:
    x = Game()
    x.name = g['name']
    x.version = g['version']
    x.acronym = g['acronym']
    x.description = g['description']
    x.alpha = g['alpha']
    x.beta = g['beta']
    x.gamma = g['gamma']
    x.save()
