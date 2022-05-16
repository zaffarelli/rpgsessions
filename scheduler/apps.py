from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        import scheduler.signals.user
        import scheduler.signals.profile
        import scheduler.signals.session
        import scheduler.signals.realm
        import scheduler.signals.campaign
        import scheduler.signals.inscription
