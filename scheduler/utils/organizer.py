from datetime import datetime, timedelta, time
from scheduler.utils.mechanics import MONTHES, DOWS


def build_month(d):
    num_week = 5
    current_month = d.month
    context = {'month_name': MONTHES[current_month - 1], 'weeks_count': num_week, 'weeks': []}

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
        bod = build_day(current_day)
        day = {'day_info': f'{DOWS[cur_day.weekday()]}<BR/><small>{cur_day.strftime("%d/%m/%y")}</small>',
               'day_off': day_off, 'current_day': current_day, 'day_body': bod}
        context['week'].append(day)
    return context


def build_day(d):
    context = {'hours': []}
    t0 = time.fromisoformat('13:00:00')
    hours = []
    for i in range(14):
        x = t0.hour + i
        x = x % 24
        t = time.fromisoformat(f'{x:02}:00:00')
        hours.append({'t': t.strftime('%H:%M')})
    context['hours'] = hours
    return context
