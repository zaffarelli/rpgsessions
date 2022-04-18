from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_TIME, FMT_DATE, FMT_DATETIME, DOWS, FMT_DATE_PRETTY
from scheduler.utils.organizer import build_month, build_zoomed_day, gimme_profile, system_flush, gimme_set_followers, \
    toggle_available, toggle_subscribe, gimme_session, gimme_profile_campaigns, gimme_profile_propositions, gimme_campaign
from datetime import datetime, date
from scheduler.utils.tools import is_ajax


def prepare_who(request, pk):
    u = gimme_profile(pk)
    context = {'fontset': FONTSET, 'u': u}
    return context


@login_required
def who(request, pk=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    if pk is None:
        pk = 1
    context = prepare_who(request,pk)
    return render(request, 'scheduler/who.html', context=context)

