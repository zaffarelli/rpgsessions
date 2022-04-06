from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scheduler.models.session import Session


@receiver(pre_save, sender=Session, dispatch_uid='prepare_session')
def prepare_session(sender, instance, **kwargs):
    if instance.realm is None:
        from scheduler.models.realm import Realm
        realms = Realm.objects.filter(is_default=True)
        if len(realms) == 1:
            instance.realm = realms.first()
    if instance.game is None:
        from scheduler.models.game import Game
        g = Game.objects.get(name='Autre')
        instance.game = g
    print("Saving session", instance.title)
