from django.contrib import admin
from django.conf.urls import include
from django.urls import path

admin.site.site_header = "eXtraventures (Administration)"
admin.site.site_title = "eXtraventures"
admin.site.index_title = "Bienvenue sur eXtraventures."

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('scheduler.urls')),
]


