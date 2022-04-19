from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scheduler.models.campaign import Campaign


@receiver(pre_save, sender=Campaign, dispatch_uid='prepare_campaign')
def prepare_campaign(sender, instance, **kwargs):
    if instance.game is None:
        from scheduler.models.game import Game
        g = Game.objects.get(name='Autre')
        instance.game = g
    # print("Saving session", instance.title)
