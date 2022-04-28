from django.core.mail import send_mail
from scheduler.utils.mechanics import FMT_DATE_PRETTY
from datetime import date, timedelta
from django.core.mail import EmailMultiAlternatives


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


def cyberpostit():
    """ Activity for the current day (if any) """
    from scheduler.models.profile import Profile
    profiles = Profile.objects.filter(mail_cyber_postit=True)
    d1 = date.today()
    d2 = date.today()
    for p in profiles:
        has_played, played_data = p.played_the(d1, d2)
        has_masterized, masterized_data = p.masterized_the(d1, d2)
        if has_played or has_masterized:
            subject = f"[eXtraventures] Cyber PostIt !"
            body = EmailBody()
            body.stack(f"Salutations {p.nickname}!")
            body.stack("")
            body.stack("Vous recevez ce message car le flag 'Cyber PostIt' est activé sur votre compte eXtraventures.")
            body.stack(
                "Vous ne recevrez ce message que si vous participez à des parties aujourd'hui. Si ce n'est pas le cas, pas de message!")
            body.stack("¤ ¤ ¤")
            body.stack("    Alors, puisque nous en somme là, c'est qu'il y a quelque chose à dire...")
            if has_played:
                body.stack("")
                body.stack(f"    (a) Parties jouées:")
                for s in played_data:
                    body.stack("")
                    body.stack(
                        f"    - {s.title} par {s.mj.nickname}, jeu=[{s.game.name}], le {s.date_start.strftime(FMT_DATE_PRETTY)} à [{s.place}] (inscription ok)")
                    body.stack(f"     Description:  {s.description} ")
                    body.stack("")
            if has_masterized:
                body.stack("")
                body.stack(f"    (b) Parties menées:")
                for s in masterized_data:
                    body.stack("")
                    body.stack(
                        f"    - [{s.title}] par {s.mj.nickname}, le {s.date_start.strftime(FMT_DATE_PRETTY)} à [{s.place}] (c'est toi le MJ!)")
                    body.stack("")
            body.stack("¤ ¤ ¤")
            body.stack(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
            sender = f'fernando.casabuentes@gmail.com'
            targets = [p.user.email]
            send_mail(subject, body.deliver(), sender, targets, fail_silently=False)
