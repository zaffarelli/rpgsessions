from django.core.mail import send_mail
from scheduler.utils.mechanics import FMT_DATE_PRETTY, FMT_TIME
from datetime import date, timedelta
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailBody(object):
    def __init__(self):
        self.pile = []
        self.json = {}

    def stack(self, txt):
        self.pile.append(txt)

    def deliver(self):
        return "\n".join(self.pile)


def week_bounds():
    date_a = date.today()
    date_b = date_a + timedelta(days=7)
    return date_a.strftime(FMT_DATE_PRETTY), date_b.strftime(FMT_DATE_PRETTY), date_a, date_b

def review_tracker_auto():
    from scheduler.models.profile import Profile
    profiles = Profile.objects.filter(tracker_auto=True)
    for p in profiles:
        p.clean_track()
        p.save()

def cyberpostit():
    """ Activity for the current day (if any) """
    from scheduler.models.profile import Profile
    from scheduler.views.gimme import gimme_profile

    profiles = Profile.objects.filter(mail_cyber_postit=True)
    d1 = date.today()
    d2 = date.today() + timedelta(days=0)
    d7 = date.today() + timedelta(days=7)
    for p in profiles:
        has_played, played_data = p.played_the(d1, d2)
        has_masterized, masterized_data = p.masterized_the(d1, d2)
        has_wanted, wanted_data = p.wanted_the(d1, d7)
        if has_played or has_masterized or has_wanted:
            print(f"Handling... {p.nickname}")
            subject = f"[eXtraventures] Cyber PostIt ! ({p.user.email})"
            email_data = {}
            email_data['nickname'] = p.nickname
            email_data['has_played'] = has_played
            email_data['has_masterized'] = has_masterized
            email_data['has_wanted'] = has_wanted
            email_data['played_data'] = []
            email_data['masterized_data'] = []
            email_data['wanted_data'] = []
            if has_played:
                for s in played_data:
                    session_data = {}
                    session_data['title'] = s.title
                    session_data['mj'] = gimme_profile(s.mj.id)
                    session_data['game'] = s.game.name
                    session_data['date'] = s.date_start.strftime(FMT_DATE_PRETTY)
                    session_data['start'] = s.time_start.strftime(FMT_TIME)
                    session_data['place'] = s.place
                    session_data['description'] = s.description
                    session_data['alert'] = False
                    email_data['played_data'].append(session_data)
            if has_masterized:
                for s in masterized_data:
                    session_data = {}
                    session_data['title'] = s.title
                    session_data['mj'] = gimme_profile(s.mj.id)
                    session_data['game'] = s.game.name
                    session_data['date'] = s.date_start.strftime(FMT_DATE_PRETTY)
                    session_data['start'] = s.time_start.strftime(FMT_TIME)
                    session_data['place'] = s.place
                    session_data['description'] = s.description
                    session_data['alert'] = False
                    email_data['masterized_data'].append(session_data)
            if has_wanted:
                for s in wanted_data:
                    session_data = {}
                    session_data['title'] = s.title
                    session_data['mj'] = gimme_profile(s.mj.id)
                    session_data['game'] = s.game.name
                    session_data['date'] = s.date_start.strftime(FMT_DATE_PRETTY)
                    session_data['start'] = s.time_start.strftime(FMT_TIME)
                    session_data['place'] = s.place
                    session_data['description'] = s.description
                    session_data['alert'] = True
                    email_data['wanted_data'].append(session_data)
            sender = f'fernando.casabuentes@gmail.com'
            targets = [p.user.email]
            # targets = ["zaffarelli@gmail.com"]
            html_message = render_to_string('scheduler/emails/cyber_postit.html', context=email_data)
            # print(email_data)
            # print(html_message)
            plain_message = strip_tags(html_message)
            mail.send_mail(subject, plain_message, f"From <{sender}>", targets, html_message=html_message)
        else:
            print("Nothing to say !!")


def wednesday():
    """ Wednesday recap of everything coming in the week """
    from scheduler.models.profile import Profile
    profiles = Profile.objects.filter(mail_wednesday=True)
    d1 = date.today()
    d2 = date.today() + timedelta(days=6)
    for p in profiles:
        has_played, played_data = p.played_the(d1, d2)
        has_masterized, masterized_data = p.masterized_the(d1, d2)
        if has_played or has_masterized:
            subject = f"[eXtraventures] Message du Mercredi !"
            body = EmailBody()
            body.stack(f"Salutations {p.nickname}!")
            body.stack("")
            body.stack(
                "Vous recevez ce message car le flag 'Message du mercredi' est activé sur votre compte eXtraventures.")
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


def sunday():
    """ Sunday recap of actions to be done """
    from scheduler.models.profile import Profile
    profiles = Profile.objects.filter(mail_sunday=True)
    d1 = date.today()
    d2 = date.today() + timedelta(days=28)
    for p in profiles:
        has_wanted, wanted_data = p.wanted_the(d1, d2)
        if has_wanted:
            subject = f"[eXtraventures] Message du Dimanche !"
            body = EmailBody()
            body.stack(f"Salutations {p.nickname}!")
            body.stack("")
            body.stack(
                "Vous recevez ce message car le flag 'Message du dimanche' est activé sur votre compte eXtraventures.")
            body.stack(
                "Vous ne recevrez ce message que si vous participez à des parties aujourd'hui. Si ce n'est pas le cas, pas de message!")
            body.stack("¤ ¤ ¤")
            # Parties Wanted sans inscription
            body.stack(
                "  Pour les parties suivantes, vous êtes sollicités, mais n'êtes pas encore inscrits dessus (dans les quatre semaines qui arrivent).")
            body.stack("  Il y a deux possibilités :")
            body.stack("  1) Vous vous inscrivez, à la partie.")
            body.stack("  2) Vous vous notez absent le jour de la partie.")
            body.stack("")
            if has_wanted:
                body.stack("")
                body.stack(f"    (a) Parties sollicité sans inscription:")
                for s in wanted_data:
                    body.stack("")
                    body.stack(
                        f"    - {s.title} par {s.mj.nickname}, jeu=[{s.game.name}], le {s.date_start.strftime(FMT_DATE_PRETTY)} à [{s.place}] (inscription ok)")
                    body.stack(f"     Description:  {s.description} ")
                    body.stack("")
            body.stack("¤ ¤ ¤")
            body.stack(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
            sender = f'fernando.casabuentes@gmail.com'
            targets = [p.user.email]
            send_mail(subject, body.deliver(), sender, targets, fail_silently=False)
