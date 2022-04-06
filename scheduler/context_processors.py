from django.conf import settings


def commons(request):
    context = {"version": settings.VERSION}
    return context
