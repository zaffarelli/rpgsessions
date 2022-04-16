from django.conf import settings
from scheduler.models.realm import Realm


def commons(request):
    realm_id = Realm.objects.first().id or 0
    context = {"version": settings.VERSION, "current_realm_id": realm_id}
    return context
