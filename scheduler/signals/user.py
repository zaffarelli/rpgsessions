from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from scheduler.models.profile import Profile


@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, **kwargs):
    all_profiles = Profile.objects.filter(user=instance)
    if len(all_profiles) == 0:
        p = Profile()
        p.user = instance
        p.nickname = instance.username
        p.save()
