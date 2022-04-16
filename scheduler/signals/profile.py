from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scheduler.models.profile import Profile
import json


@receiver(pre_save, sender=Profile, dispatch_uid='prepare_svg_artefact')
def prepare_svg_artefact(sender, instance, **kwargs):
    # str = json.dumps(instance.build_svg_artefact(), indent=4, sort_keys=True)
    # instance.svg_artefact = str

    if not instance.realm:
        from scheduler.models.realm import Realm
        realm = Realm.objects.first()
        instance.realm = realm




