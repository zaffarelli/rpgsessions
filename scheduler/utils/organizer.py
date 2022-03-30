from datetime import datetime, timedelta, time, date
from django.template.loader import get_template
from scheduler.utils.mechanics import MONTHS, MONTHS_COLORS, MONTHS_COLORS_TEXT, DOWS, HOUR_PIXELS, FONTSET, FMT_TIME, \
    FMT_DATE, \
    FMT_DATETIME, FMT_DATE_PRETTY


def gimme_session(request, s):
    context = s.to_json
    context['episode_tag'] = s.episode_tag
    context['user_wanted'] = s.wanted_list
    context['max_players'] = s.max_players
    if s.campaign:
        context['campaign'] = s.campaign.to_json
    return context


def gimme_day(request, d):
    is_current_day = (d.strftime(FMT_DATE) == datetime.today().strftime(FMT_DATE))
    day_body = {}
    day_body['sessions'] = gimme_sessions_of_the_day(request, d)
    context = {'day_info': f'{DOWS[d.weekday()]}<BR/><small>{d.strftime(FMT_DATE_PRETTY)}</small>',
               'day_off': d.weekday() > 4,
               'current_day': is_current_day,
               'day': d.strftime(FMT_DATE),
               'day_body': day_body,
               'month_color': MONTHS_COLORS[d.month - 1]
               }
    context['availabilities'] = gimme_all_availabilities(request, d, request.user.profile.id)
    return context


def gimme_sessions_of_the_day(request, d):
    from scheduler.models.session import Session
    all = Session.objects.filter(date_start=d).order_by('time_start')
    sessions = []
    for s in all:
        user_wanted = s.wanted.split(';')
        sess = {
            's': s.to_json,
            'user_wanted': str(request.user.profile.id) in user_wanted,
            'u': gimme_profile(s.mj.id),
            'g': s.game.to_json
        }
        sessions.append(sess)
    return sessions


# def gimme_all_followers(id):
#     from scheduler.models.follower import Follower
#     context = {}
#     f_list = []
#     all_profiles = Profile.objects.all().order_by('profile__user_id')
#     all_followers = Follower.objects.filter(profile__user_id=id)
#     for f in all_followers:
#         f_list.add(f.target.user_id)
#     for p in all_profiles:
#         context.append({'profile': gimme_profile(p), 'is_follower': p.user_id in f_list})
#     return context


def gimme_all_availabilities(request, d, id):
    from scheduler.models.availability import Availability
    from scheduler.models.follower import Follower
    context = {}
    availables = []
    absents = []
    absents_title = []
    availables_title = []
    my_followers = []
    all_followers = Follower.objects.filter(profile__user_id=id)
    for f in all_followers:
        my_followers.append(f.target.id)
    here_entries = Availability.objects.filter(when=d, absent_mode=False)

    for here in here_entries:
        if here.profile.id in my_followers:
            availables.append(gimme_profile(here.profile.id))
            availables_title.append(gimme_profile(here.profile.id)['nickname'])
    off_entries = Availability.objects.filter(when=d, absent_mode=True)
    # if len(off_entries) > 0:
    #     print(all_followers, my_followers, off_entries)
    for off in off_entries:
        if off.profile.id in my_followers:
            absents.append(gimme_profile(off.profile.id))
            absents_title.append(gimme_profile(off.profile.id)['nickname'])

    context['availables'] = availables
    context['absents'] = absents
    if len(absents_title) > 0:
        context['absents_title'] = "Absent(es): " + ', '.join(absents_title)
    else:
        context['absents_title'] = 'Rien à signaler'
    if len(availables_title) > 0:
        context['availables_title'] = "Disponible(s): " + ', '.join(availables_title)
    else:
        context['availables_title'] = 'Rien à signaler'
    return context


def gimme_profile(x):
    from scheduler.models.profile import Profile
    elem = Profile.objects.get(pk=x)
    context = {'Status': f'The parameter {x} is not a user profile'}
    # print(elem)
    if isinstance(elem, Profile):
        context = elem.to_json
        context['status'] = "ok"
        context['silhouette_symbol'] = elem.silhouette_symbol
        context['shield_symbol'] = elem.shield_symbol
    return context


# Root functions called from views
def build_month(request, date_str):
    d = date.fromisoformat(date_str)
    num_week = 5
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


# def build_day(request, d):
#     context = {}
#     cur_date = date.fromisoformat(d.strftime(FMT_DATE))
#     context['day'] = gimme_day(cur_date)
#     context['availabilities'] = gimme_all_availabilities(cur_date, request.user.profile_id)
#     print(context)
#     return context


def build_zoomed_day(request, d):
    from scheduler.models.session import Session
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
        inscriptions = []
        for i in s.inscription_set.all().order_by('profile__user_id'):
            inscriptions.append(gimme_profile(i.profile.id))
        sess = {'s': gimme_session(request, s),
                'u': gimme_profile(s.mj.id),
                'inscriptions': inscriptions,
                'g': s.game.to_json,
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


def system_flush():
    from scheduler.models.availability import Availability
    data_from_the_past = Availability.objects.filter(when__lt=datetime.today())
    for i in data_from_the_past:
        i.delete()


def gimme_set_followers(id):
    from scheduler.models.follower import Follower
    from scheduler.models.profile import Profile
    f_list = []
    list = []
    it = Profile.objects.get(pk=id)
    all_profiles = Profile.objects.order_by('nickname')
    all_followers = Follower.objects.filter(profile=it)
    for f in all_followers:
        f_list.append(f.target.id)
    for p in all_profiles:
        list.append({'profile': gimme_profile(p.id), 'is_follower': p.id in f_list})
    return list


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
    from scheduler.views.base import prepare_session

    profile = request.user.profile
    sessions = Session.objects.filter(id=int(param))
    if len(sessions) == 1:
        inscriptions = Inscription.objects.filter(profile=profile, session=sessions.first())
        if len(inscriptions) == 1:
            print("Unsubscribing")
            f = inscriptions.first()
            f.delete()
        else:
            print("Subscribing")
            n = Inscription()
            n.profile = profile
            n.session = sessions.first()
            n.pending = True
            n.save()
    context = prepare_session(request, int(param))
    template = get_template("scheduler/session_details.html")
    html = template.render(context, request)
    target = '.day_details'
    return html, target
