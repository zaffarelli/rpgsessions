from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scheduler.models.realm import Realm
import json


@receiver(pre_save, sender=Realm, dispatch_uid='prepare_realm')
def prepare_realm(sender, instance, **kwargs):
    instance.full_link = f'invite/{instance.invite_link}/'




