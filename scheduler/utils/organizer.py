from datetime import datetime, timedelta, time, date
from scheduler.utils.mechanics import MONTHS, MONTHS_COLORS, MONTHS_COLORS_TEXT, DOWS, HOUR_PIXELS, FONTSET, FMT_TIME, \
    FMT_DATE, \
    FMT_DATETIME, FMT_DATE_PRETTY


def gimme_day(d):
    is_current_day = (d.strftime(FMT_DATE) == datetime.today().strftime(FMT_DATE))
    day_body = {}
    day_body['sessions'] = gimme_sessions_of_the_day(d)
    context = {'day_info': f'{DOWS[d.weekday()]}<BR/><small>{d.strftime(FMT_DATE_PRETTY)}</small>',
               'day_off': d.weekday() > 4,
               'current_day': is_current_day,
               'day': d.strftime(FMT_DATE),
               'day_body': day_body,
               'month_color': MONTHS_COLORS[d.month - 1]
               }
    return context


def gimme_sessions_of_the_day(d):
    from scheduler.models.session import Session
    all = Session.objects.filter(date_start=d).order_by('time_start')
    sessions = []
    for s in all:
        sess = {
            's': s.to_json,
            'u': gimme_profile(s.mj),
            'g': s.game.to_json
        }
        sessions.append(sess)
    return sessions


def gimme_all_followers(id):
    from scheduler.models.follower import Follower
    context = {}
    f_list = []
    all_profiles = Profile.objects.all().order_by('profile__user_id')
    all_followers = Follower.objects.filter(profile__user_id=id)
    for f in all_followers:
        f_list.add(f.target.user_id)
    for p in all_profiles:
        context.append({'profile': gimme_profile(p), 'is_follower': p.user_id in f_list})
    return context


def gimme_all_availabilities(d):
    from scheduler.models.availability import Availability
    context = {}
    availables = []
    absents = []
    here_entries = Profile.objects.filter(when=date(d)).order_by('profile__user_id', absent_mode=False)
    for here in here_entries:
        availables.append(gimme_profile(here))
    off_entries = Profile.objects.filter(when=date(d)).order_by('profile__user_id', absent_mode=True)
    for off in off_entries:
        absents.append(gimme_profile(off))
    context['availables'] = availables
    context['absents'] = absents
    return context


def gimme_profile(x):
    from scheduler.models.profile import Profile
    context = {'Status': f'The parameter {x} is not a user profile'}
    if isinstance(x, Profile):
        context = x.to_json
        context['status']: ok
        context['silhouette_symbol'] = x.silhouette_symbol
        context['shield_symbol'] = x.shield_symbol

    return context


def build_month(date_str):
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
               'weeknext': weeknext.strftime(FMT_DATE),
               'monthnext': monthnext.strftime(FMT_DATE)
               }
    weeks_back = 1
    first_day = d - timedelta(days=weeks_back * 7)
    weeks = []
    for i in range(num_week):
        w = build_week(first_day + timedelta(days=i * 7))
        weeks.append(w)
    context['weeks'] = weeks
    return context


def build_week(d):
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
        day = gimme_day(cur_day)
        context['week'].append(day)
    return context


def build_day(d):
    context = {}
    cur_date = date.fromisoformat(d.strftime(FMT_DATE))
    # context['sessions'] = gimme_sessions_of_the_day(cur_date)
    context['day'] = gimme_day(cur_date)
    return context

def gimme_session(s):
    context = s.to_json
    context['episode_tag'] = s.episode_tag
    print(context)
    return context

def build_zoomed_day(d):
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
            inscriptions.append(gimme_profile(i.profile))
        sess = {'s': gimme_session(s),
                'u': gimme_profile(s.mj),
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
    day = gimme_day(cur_date)
    context['day'] = day
    return context
