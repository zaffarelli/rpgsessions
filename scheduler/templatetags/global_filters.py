from django import template
from datetime import time, date
from scheduler.utils.mechanics import FMT_TIME, FMT_DATE

register = template.Library()

@register.filter(name='as_day_off')
def as_day_off(value):
    res = ''
    if value:
        res = 'day_off'
    # print(str(value))
    return res


@register.filter(name='as_current_day')
def as_current_day(value):
    res = ''
    if value:
        res = 'current_day'
    return res


@register.filter(name='as_bool')
def as_bool(value):
    res = '<span style="color:red;"><i class="fas fa-times-circle"></i></span>'
    if str(value)[0] in ['T', 't', '0', '1']:
        res = '<span style="color:green;"><i class="fas fa-check-circle"></i></span>'
    return res


@register.filter(name='as_gender')
def as_gender(value):
    res = '<span style="color:maroon;"><i class="fas fa-mars"></i></span>'
    if str(value)[0] in ['T', 't', '0', '1']:
        res = '<span style="color:violet;"><i class="fas fa-venus"></i></span>'
    return res


@register.filter(name='as_time')
def as_time(value):
    t = time(hour=value['hour'], minute=value['minute'])
    res = t.strftime(FMT_TIME)
    return res


@register.filter(name='as_date')
def as_date(value):
    if value:
        d = date(year=value['year'], month=value['month'], day=value['day'])
        res = d.strftime(FMT_DATE)
    else:
        res = "Proposition!"
    return res

@register.filter(name='as_date_schedule')
def as_date_schedule(value):
    import datetime
    now = datetime.date.today()
    if value:
        d = date(year=value['year'], month=value['month'], day=value['day'])
        if d < now:
            schedule = "past"
        else:
            schedule = "future"
        res = "<span class='"+schedule+"'>"+d.strftime(FMT_DATE)+"</span>"
    else:
        res = "Proposition!"
    return res


@register.filter(name='as_level')
def as_level(value):
    from scheduler.utils.mechanics import ADV_LEVEL
    res = '?'
    if str(value) != '':
        res = ADV_LEVEL[int(value)][1]
    return res


@register.filter(name='as_icon_style')
def as_icon_style(value):
    return res


@register.filter(name='boolean')
def boolean(value):
    if str(value).lower() in ["true", "1", "yes"]:
        return True
    else:
        return False
