from django import template
import datetime

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