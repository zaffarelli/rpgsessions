from datetime import datetime, timedelta, time, date
from django.template.loader import get_template
from scheduler.utils.mechanics import MONTHS, MONTHS_COLORS, MONTHS_COLORS_TEXT, HOUR_PIXELS, FMT_TIME, FMT_DATE
from scheduler.views.gimme import gimme_profile, gimme_session, gimme_day, gimme_all_availabilities


def prepare_session(request, id=None):
    from scheduler.models.session import Session
    all = Session.objects.filter(pk=id)
    cur_date = datetime.now()
    context = {'status': 'KO'}
    if len(all) == 1:
        context['status'] = 'OK'
        that = all.first()
        inscriptions = []
        for i in that.inscription_set.all().order_by('profile__user_id'):
            inscriptions.append(gimme_profile(i.profile.id))
        context['session'] = gimme_session(request, that)
        context['game'] = that.game.to_json
        context['mj'] = gimme_profile(that.mj.id)
        context['owner'] = that.mj.user == request.user
        context['wanted_list'] = that.wanted_list
        context['inscriptions'] = inscriptions
        context['availabilities'] = gimme_all_availabilities(request, cur_date, request.user.profile.id)
    context['day'] = gimme_day(request, cur_date)
    return context


def prepare_month(request, slug=None):
    if slug is None:
        d = datetime.now()
    else:
        slug = slug.replace("_", "-")
        d = date.fromisoformat(slug)
    m = build_month(request, d.strftime(FMT_DATE))
    context = {'c': m}
    return context


def prepare_day(request, slug=None):
    slug = slug.replace('_', '-')
    d = date.fromisoformat(slug)
    data = build_zoomed_day(request, d)
    context = {'data': data}
    return context

# Root functions called from views
def build_month(request, date_str):
    d = date.fromisoformat(date_str)
    num_week = 3 + request.user.profile.weeks
    current_month = d.month
    monthback = d - timedelta(days=28)
    weekback = d - timedelta(days=7)
    weeknext = d + timedelta(days=7)
    monthnext = d + timedelta(days=28)

    context = {'month_name': f'{MONTHS[current_month - 1]} {d.strftime("%Y")}',
               'month_color': MONTHS_COLORS[current_month - 1],
               'month_color_text': MONTHS_COLORS_TEXT[current_month - 1],
               'weeks_count': num_week,
               'date': d.strftime(FMT_DATE),
               'monthback': monthback.strftime(FMT_DATE),
               'weekback': weekback.strftime(FMT_DATE),
               'today': datetime.now().strftime(FMT_DATE),
               'weeknext': weeknext.strftime(FMT_DATE),
               'monthnext': monthnext.strftime(FMT_DATE)
               }
    weeks_back = 1
    first_day = d - timedelta(days=weeks_back * 7)
    weeks = []
    for i in range(num_week):
        w = build_week(request, first_day + timedelta(days=i * 7))
        weeks.append(w)
    context['weeks'] = weeks
    return context


def build_week(request, d):
    context = {}
    context['week_number'] = d.isocalendar()[1]
    dprev = d - timedelta(days=7)
    context['week_number_prev'] = dprev.isocalendar()[1]
    dow = d.weekday()
    # 2 3 4 5 6 0 1
    # M J V S D L M
    day0 = d
    if dow < 2:
        day0 = d - timedelta(days=5 + dow)
    elif dow > 2:
        day0 = d - timedelta(days=(dow - 2))
    context['week'] = []
    for x in range(7):
        cur_day = day0 + timedelta(days=x)
        day = gimme_day(request, cur_day)
        context['week'].append(day)
    return context


def build_zoomed_day(request, d):
    from scheduler.models.session import Session
    from scheduler.views.gimme import gimme_game, gimme_inscriptions
    cur_date = date.fromisoformat(d.strftime(FMT_DATE))
    all = Session.objects.filter(date_start=cur_date).order_by('time_start')
    context = {}
    sessions = []
    for s in all:
        delta = datetime.combine(cur_date, s.time_start) - datetime.combine(cur_date, time.fromisoformat('13:00:00'))
        pre_size = delta.total_seconds() / 3600 * HOUR_PIXELS
        # print(s.time_start, delta, delta.total_seconds(), ":", pre_size)
        size = s.duration * HOUR_PIXELS
        post_size = 14 * HOUR_PIXELS - pre_size - size
        # print(pre_size/HOUR_PIXELS, size/HOUR_PIXELS, post_size/HOUR_PIXELS)
        # inscriptions = []
        # for i in s.inscription_set.all().order_by('profile__user_id'):
        #     inscriptions.append(gimme_profile(i.profile.id))
        sess = {'s': gimme_session(request, s),
                'u': gimme_profile(s.mj.id),
                'inscriptions': gimme_inscriptions(s),
                'g': gimme_game(s.game),
                'timescale': {
                    'pre_size': pre_size,
                    'size': size,
                    'post_size': post_size,
                }
                }
        sessions.append(sess)
    context['sessions'] = sessions
    t0 = time.fromisoformat('13:00:00')
    hours = []
    for i in range(14):
        x = t0.hour + i
        x = x % 24
        t = time.fromisoformat(f'{x:02}:00:00')
        hours.append({'t': t.strftime(FMT_TIME)})
    context['hours'] = hours
    context['day'] = gimme_day(request, cur_date)
    context['availabilities'] = gimme_all_availabilities(request, cur_date, request.user)
    return context


def toggle_available(request, action, param):
    from scheduler.models.availability import Availability
    date_str = param.replace('_', '-')
    cur_date = date.fromisoformat(date_str)
    new_mode = action == 'set_absent'
    all = Availability.objects.filter(when=cur_date, profile=request.user.profile)
    if len(all) == 0:
        n = Availability()
        n.when = cur_date
        n.profile = request.user.profile
        n.absent_mode = new_mode
        n.save()
    elif len(all) == 1:
        f = all.first()
        if f.absent_mode == new_mode:
            f.delete()
        else:
            f.absent_mode = new_mode
            f.save()
    else:
        for a in all:
            a.delete()
        n = Availability(when=cur_date, profile=request.user.profile)
        n.absent_mode = new_mode
        n.save()
    context = {'data': {}}
    context['data']['availabilities'] = gimme_all_availabilities(request, cur_date, request.user.profile.id)
    template = get_template("scheduler/day_availabilities.html")
    target = '.day_details'
    html = template.render(context, request)
    return html, target


def toggle_subscribe(request, action, param):
    from scheduler.models.inscription import Inscription
    from scheduler.models.session import Session
    # from scheduler.views.base import prepare_session

    profile = request.user.profile
    sessions = Session.objects.filter(id=int(param))
    if len(sessions) == 1:
        s = sessions.first()
        inscriptions = Inscription.objects.filter(session=sessions.first())
        my_inscription = Inscription.objects.filter(profile=profile, session=sessions.first())
        max_players = s.optional_spots + len(s.wanted_list)
        if len(inscriptions) < max_players:
            if len(my_inscription) == 1:
                f = inscriptions.first()
                f.delete()
            else:
                n = Inscription()
                n.profile = profile
                n.session = sessions.first()
                n.pending = True
                n.save()
        else:
            print("No more room for inscriptions..")
    context = prepare_session(request, int(param))
    template = get_template("scheduler/session_detail.html")
    html = template.render(context, request)
    target = '.day_details'
    return html, target
