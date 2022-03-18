from datetime import datetime, timedelta, time, date
from scheduler.utils.mechanics import MONTHS, MONTHS_COLORS, DOWS, HOUR_PIXELS


def build_month(d, day_offset=0):
    num_week = 5
    current_month = d.month
    context = {'month_name': MONTHS[current_month - 1], 'weeks_count': num_week, 'weeks': []}

    current_day = d.day
    weeks_back = int(current_day / 7)
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
        day_off = cur_day.weekday() > 4
        current_day = cur_day.day == datetime.today().day
        bod = build_day(cur_day)
        day = {'day_info': f'{DOWS[cur_day.weekday()]}<BR/><small>{cur_day.strftime("%d/%m/%y")}</small>',
               'day_off': day_off,
               'current_day': current_day,
               'day': cur_day.strftime("%Y-%m-%d"),
               'day_body': bod,
               'month_color': MONTHS_COLORS[cur_day.month]
               }
        context['week'].append(day)
    return context


def build_day(d):
    from scheduler.models.session import Session
    cur_date = date.fromisoformat(f'{d.year:04}-{d.month:02}-{d.day:02}')
    all = Session.objects.filter(date_start=cur_date).order_by('time_start')
    context = {}
    sessions = []
    for s in all:
        sess = {'title': s.title, 'date': s.date_start, 'time': s.time_start, 'mj': s.mj.to_json,
                'game': {'name': s.game.name, 'acro': s.game.acronym, 'alpha': s.game.alpha, 'beta': s.game.beta,
                         'gamma': s.game.gamma}}
        sessions.append(sess)
    context['sessions'] = sessions
    return context


def build_zoomed_day(d):
    from scheduler.models.session import Session
    cur_date = date.fromisoformat(f'{d.year:04}-{d.month:02}-{d.day:02}')
    all = Session.objects.filter(date_start=cur_date).order_by('time_start')
    context = {}
    sessions = []
    for s in all:
        delta = datetime.combine(cur_date, s.time_start) - datetime.combine(cur_date, time.fromisoformat('13:00:00'))
        pre_size = delta.total_seconds() / 3600 * HOUR_PIXELS
        # print(s.time_start, delta, delta.total_seconds(), ":", pre_size)
        size = s.duration * HOUR_PIXELS
        post_size = 14 * HOUR_PIXELS - pre_size - size
        inscriptions = []
        for i in s.inscription_set.all():
            inscriptions.append(i.profile.to_json)
        sess = {'title': s.title, 'date': s.date_start, 'time': s.time_start, 'mj': s.mj.to_json, 's': s.to_json,
                'inscriptions': inscriptions,
                'game': {'name': s.game.name,
                         'acro': s.game.acronym,
                         'alpha': s.game.alpha,
                         'beta': s.game.beta,
                         'gamma': s.game.gamma,
                         'pre_size': pre_size,
                         'size': size,
                         'post_size': post_size,
                         }}
        sessions.append(sess)
    context['sessions'] = sessions
    t0 = time.fromisoformat('13:00:00')
    hours = []
    for i in range(14):
        x = t0.hour + i
        x = x % 24
        t = time.fromisoformat(f'{x:02}:00:00')
        hours.append({'t': t.strftime('%H:%M')})
    context['hours'] = hours
    day_off = cur_date.weekday() > 4
    current_day = cur_date.day == datetime.today().day
    day = {'date': cur_date, 'day_off': day_off, 'current_day': current_day,
           'day_info': f'{DOWS[cur_date.weekday()]}<BR/><small>{cur_date.strftime("%d/%m/%y")}</small>'}
    context['day'] = day
    return context
