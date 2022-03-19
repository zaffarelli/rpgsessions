from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from scheduler.utils.mechanics import FONTSET, FMT_TIME, FMT_DATE, FMT_DATETIME
from scheduler.utils.organizer import build_month, build_zoomed_day
from datetime import datetime, date


def prepare_index(request):
    d = datetime.now()
    m = build_month(d.strftime(FMT_DATE))
    context = {'fontset': FONTSET, 'month': m}
    return context


@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_index(request)
    return render(request, 'scheduler/index.html', context=context)


def prepare_day(request, slug=None):
    slug = slug.replace('_', '-')
    d = date.fromisoformat(slug)
    data = build_zoomed_day(d)
    context = {'data': data}
    return context


@login_required
def display_day(request, slug=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_day(request, slug)
    template = get_template('scheduler/menu_dayzoom.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/day_zoom.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def prepare_month(request, slug=None):
    if slug is None:
        d = datetime.now()
    else:
        slug = slug.replace("_", "-")
        d = date.fromisoformat(slug)
    m = build_month(d.strftime(FMT_DATE))
    context = {'c': m}
    return context


@login_required
def display_month(request, slug=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_month(request, slug)
    template = get_template('scheduler/menu_month.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/month.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


def prepare_session(request,id=None):
    from scheduler.models.session import Session
    all = Session.objects.filter(pk=id)
    context = {'status': 'KO'}
    if len(all) == 1:
        context['status'] = 'OK'
        that = all.first()
        context['session'] = that.to_json
        context['game'] = that.game.to_json
        context['mj'] = that.mj.to_json
        context['owner'] = that.mj.user == request.user
    return context


@login_required
def display_session(request, id=None):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = prepare_session(request,id)
    html = 'WTF?'
    menu_html = 'WTF?'
    if context['status'] == 'OK':
        template = get_template('scheduler/menu_session.html')
        menu_html = template.render(context, request)
        template = get_template('scheduler/session_details.html')
        html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)
