import datetime


def json_default(value):
    import datetime
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute,
                    second=value.second)
    elif isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, datetime.time):
        return dict(hour=value.hour, minute=value.minute, second=value.second)
    else:
        return value.__dict__


FONTSET = ['Quicksand', 'Fredoka', 'Syne+Mono', 'Abel', 'Satisfy', 'Acme', 'Roboto', 'Hubballi','Gruppo']

MONTHS = ['JANVIER', 'FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE',
          'DECEMBRE']

MONTHS_COLORS = ["#bc2b95",
                 "#8d2094",
                 "#5d1793",
                 "#1553cc",
                 "#4db1c0",
                 "#41962a",
                 "#7fc83d",
                 "#fffe54",
                 "#f9cd46",
                 "#f39d39",
                 "#ef6f2e",
                 "#ec3323"
                 ]

DOWS = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI', 'DIMANCHE']

HOUR_PIXELS = 32
