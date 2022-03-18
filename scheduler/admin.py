from django.contrib import admin

# Register your models here.
from scheduler.models.session import Session, SessionAdmin
admin.site.register(Session, SessionAdmin)

from scheduler.models.game import Game, GameAdmin
admin.site.register(Game, GameAdmin)

from scheduler.models.realm import Realm, RealmAdmin
admin.site.register(Realm, RealmAdmin)

from scheduler.models.profile import Profile, ProfileAdmin
admin.site.register(Profile, ProfileAdmin)

from scheduler.models.inscription import Inscription, InscriptionAdmin
admin.site.register(Inscription, InscriptionAdmin)

from scheduler.models.availability import Availability, AvailabilityAdmin
admin.site.register(Availability, AvailabilityAdmin)

from scheduler.models.follower import Follower, FollowerAdmin
admin.site.register(Follower, FollowerAdmin)