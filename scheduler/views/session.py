from django.shortcuts import render
from scheduler.models.session import Session
from scheduler.forms.session_form import SessionForm


def create_session(request, slug, param=None):
    context = {}
    form = SessionForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "scheduler/session_create.html", context)
