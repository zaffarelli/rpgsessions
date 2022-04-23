from django.core.mail import send_mail
from scheduler.utils.mechanics import FMT_DATE_PRETTY
from datetime import date, timedelta

class EmailBody(object):
    def __init__(self):
        self.pile = []

    def stack(self, txt):
        self.pile.append(txt)

    def deliver(self):
        return "\n".join(self.pile)


def week_bounds():
    date_a = date.today()
    date_b = date_a + timedelta(days=7)
    return date_a.strftime(FMT_DATE_PRETTY), date_b.strftime(FMT_DATE_PRETTY), date_a, date_b


def mercure():
    from scheduler.models.session import Session
    from scheduler.models.profile import Profile
    from scheduler.models.inscription import Inscription

    profiles = Profile.objects.filter(mail_wednesday=True)
    a, b, _da, _db = week_bounds()
    for p in profiles:
        subject = f"[eXtraventures] La lettre de Mercure"
        body = EmailBody()
        body.stack(f"Salutations {p.nickname}!")
        body.stack("Tu reçois ce message car le flag 'Message du Mercredi' est activé sur ton compte eXtraventures.")
        body.stack("¤ ¤ ¤")

        body.stack(f"(1) Informations sur la semaine à venir, du {a} au {b}:")
        body.stack(f"    (a) Parties jouées:")

        inscriptions = Inscription.objects.filter(profile=p)
        inscription_set = []
        for i in inscriptions:
            if _da <= i.session.date_start <= _db:
                inscription_set.append(i.session.id)
        sessions = Session.objects.filter(date_start__gte=_da, date_start__lte=_db)
        for s in sessions:
            if s.id in inscription_set:
                body.stack(f"    - {s.title} par {s.mj.nickname}, le f{s.date_start.strftime(FMT_DATE_PRETTY)} à {s.place} (inscription ok)")
        body.stack(f"    (b) Parties menées:")
        sessions_mj = Session.objects.filter(date_start_gte=_da, date_start_lte=_db, mj=p)
        for s in sessions_mj:
            body.stack(f"    - {s.title} par {s.mj.nickname}, le f{s.date_start.strftime(FMT_DATE_PRETTY)} à {s.place} (c'est toi le MJ!)")
        body.stack(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
        sender = f'fernando.casabuentes@gmail.com'
        targets = [f'zaffarelli@gmail.com']
        send_mail(subject, body.deliver(), sender, targets, fail_silently=False)


