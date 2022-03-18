import datetime


def json_default(value):
    import datetime
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute, second=value.second)
    elif isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, datetime.time):
        return dict(hour=value.hour, minute=value.minute, second=value.second)
    else:
        return value.__dict__


FONTSET = ['Quicksand', 'Fredoka', 'Syne+Mono', 'Abel', 'Satisfy', 'Acme']

MONTHES = ['JANVIER', 'FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE',
           'DECEMBRE']

DOWS = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI', 'DIMANCHE']

HOUR_PIXELS = 32