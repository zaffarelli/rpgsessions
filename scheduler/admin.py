from django.contrib import admin

# Register your models here.
from scheduler.models.session import Session, SessionAdmin
admin.site.register(Session, SessionAdmin)
