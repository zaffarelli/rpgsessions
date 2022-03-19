from django import template
from datetime import time
from scheduler.utils.mechanics import FMT_TIME

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
    if value == True:
        res = '<span style="color:green;"><i class="fas fa-check-circle"></i></span>'
    return res


@register.filter(name='as_time')
def as_time(value):
    t = time(hour=value['hour'], minute=value['minute'])
    res = t.strftime(FMT_TIME)
    return res


@register.filter(name='as_level')
def as_level(value):
    from scheduler.utils.mechanics import ADV_LEVEL
    res = ADV_LEVEL[int(value)][1]
    return res
