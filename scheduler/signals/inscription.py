from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scheduler.models.inscription import Inscription


@receiver(pre_save, sender=Inscription, dispatch_uid='propagate_inscription')
def propagate_inscription(sender, instance, **kwargs):
    instance.propagate()
