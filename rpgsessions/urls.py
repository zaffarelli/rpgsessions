from django.contrib import admin
from django.conf.urls import include
from django.urls import path

admin.site.site_header = "RPGSessions (Administration)"
admin.site.site_title = "RPGSessions"
admin.site.index_title = "Welcome to the RPGSessions."

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduler.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


