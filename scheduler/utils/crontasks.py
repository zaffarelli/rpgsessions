from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail


class WednesdayCronJob(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scheduler.wednesday_cron_job'  # a unique code

    def do(self):
        subject = "[eXtraventures] La lettre du Mercredi"
        body = f"::Mouhahahahahahaha::\n\nVotre serviteur, Fernando Casabuentes"
        sender = f'fernando.casabuentes@gmail.com'
        targets = [f'zaffarelli@gmail.com']
        send_mail(subject, body, sender, targets, fail_silently=False)
