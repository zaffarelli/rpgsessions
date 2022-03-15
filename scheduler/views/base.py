from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scheduler.utils.mechanics import FONTSET
from scheduler.utils.organizer import build_month
from datetime import datetime


def prepare_index(request):
    m = build_month(datetime.now())
    context = {'fontset': FONTSET, 'month': m}
    return context


@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_index(request)
    return render(request, 'scheduler/index.html', context=context)
