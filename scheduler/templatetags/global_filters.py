from django import template
from datetime import time, date
from scheduler.utils.mechanics import FMT_TIME, FMT_DATE

register = template.Library()


# Date & Time functions
# @register.filter(name='as_date')
# def as_date(value):
#     return value.strftime("%A %d/%m/%y")
#
#
# @register.filter(name='as_time')
# def as_time(value):
#     return value.strftime("%H:%M")


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
    # print(str(value))
    return res


@register.filter(name='as_bool')
def as_bool(value):
    res = '<span style="color:red;"><i class="fas fa-times-circle"></i></span>'
    # print(value)
    if str(value)[0] in ['T', 't', '0', '1']:
        res = '<span style="color:green;"><i class="fas fa-check-circle"></i></span>'
    return res

@register.filter(name='as_gender')
def as_gender(value):
    res = '<span style="color:orange;"><i class="fas fa-mars"></i></span>'
    # print(value)
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
    d = date(year=value['year'], month=value['month'], day=value['day'])
    res = d.strftime(FMT_DATE)
    return res


@register.filter(name='as_level')
def as_level(value):
    from scheduler.utils.mechanics import ADV_LEVEL
    res = '?'
    if isinstance(value, int):
        res = ADV_LEVEL[int(value)][1]
    return res

