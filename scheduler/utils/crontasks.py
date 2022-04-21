from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from scheduler.utils.mechanics import FMT_DATE_PRETTY
from datetime import date, timedelta


class Wednesday(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scheduler.utils.crontasks.Wednesday'  # a unique code

    def do(self):
        subject = "[eXtraventures] La lettre du Mercredi"
        body_list = ["Salutations matinales !"]
        a, b = self.week_bounds()
        body_list.append(f"(1) Informations sur la semaine à venir, du {a} au {b}:")

        body_list.append(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
        body = "\n".join(body_list)
        sender = f'fernando.casabuentes@gmail.com'
        targets = [f'zaffarelli@gmail.com']
        send_mail(subject, body, sender, targets, fail_silently=False)

    def week_bounds(self):
        date_a = date.today()
        date_b = date_a + timedelta(days=7)
        return date_a.strftime(FMT_DATE_PRETTY), date_b.strftime(FMT_DATE_PRETTY)


class Sunday(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scheduler.utils.crontasks.Sunday'  # a unique code

    def do(self):
        subject = "[eXtraventures] La lettre du Dimanche"
        body_list = ["Salutations du soir !"]
        a, b = self.week_bounds()
        body_list.append(f"(1) Informations sur la semaine à venir, du {a} au {b}:")

        body_list.append(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
        body = "\n".join(body_list)
        sender = f'fernando.casabuentes@gmail.com'
        targets = [f'zaffarelli@gmail.com']
        send_mail(subject, body, sender, targets, fail_silently=False)

    def week_bounds(self):
        date_a = date.today()
        date_b = date_a + timedelta(days=7)
        return date_a.strftime(FMT_DATE_PRETTY), date_b.strftime(FMT_DATE_PRETTY)


class Hermes(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scheduler.utils.crontasks.Hermes'  # a unique code

    def do(self):
        subject = "[eXtraventures] La lettre d'Hermes'"
        body_list = ["Salutations du soir !"]
        a, b = self.week_bounds()
        body_list.append(f"(1) Informations sur la semaine à venir, du {a} au {b}:")

        body_list.append(f"::mouhahahahahahaha::\n\nVotre dévoué serviteur eXtraordinaire,\nFernando Casabuentes.")
        body = "\n".join(body_list)
        sender = f'fernando.casabuentes@gmail.com'
        targets = [f'zaffarelli@gmail.com']
        send_mail(subject, body, sender, targets, fail_silently=False)

    def week_bounds(self):
        date_a = date.today()
        date_b = date_a + timedelta(days=7)
        return date_a.strftime(FMT_DATE_PRETTY), date_b.strftime(FMT_DATE_PRETTY)
