from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import get_template
from scheduler.utils.mechanics import FMT_DATE
from scheduler.views.gimme import gimme_profile, gimme_campaign, gimme_all_propositions
from datetime import datetime


# List of all members
@login_required
def members(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    from scheduler.models.profile import Profile
    context = {}
    context['members'] = []
    context['today'] = datetime.now().strftime(FMT_DATE)
    members = Profile.objects.order_by('nickname')
    for m in members:
        context['members'].append(gimme_profile(m.id))
    template = get_template('scheduler/menu_propositions.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/all_members.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


# List of all campaigns
@login_required
def campaigns(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    from scheduler.models.campaign import Campaign
    context = {}
    context['campaigns'] = []
    context['today'] = datetime.now().strftime(FMT_DATE)
    campaigns = Campaign.objects.filter(is_visible=True).order_by('title')
    for c in campaigns:
        context['campaigns'].append(gimme_campaign(c.id))
    template = get_template('scheduler/menu_propositions.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/all_campaigns.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)


# List of all propositions
@login_required
def propositions(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    context = {}
    context['today'] = datetime.now().strftime(FMT_DATE)
    context['propositions'] = gimme_all_propositions(request, request.user.profile.id)
    template = get_template('scheduler/menu_propositions.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/all_propositions.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)

# List of all campaigns
@login_required
def news(request):
    if not request.user.is_authenticated:
        return render(request, 'scheduler/registration/login_error.html')
    from scheduler.models.campaign import Campaign
    context = {}
    context['today'] = datetime.now().strftime(FMT_DATE)
    context['incoming_games'] = request.user.profile.fetch_week_sessions()
    template = get_template('scheduler/menu_propositions.html')
    menu_html = template.render(context, request)
    template = get_template('scheduler/news.html')
    html = template.render(context, request)
    response = {'data': html, 'menu': menu_html}
    return JsonResponse(response)
