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

MONTHS_COLORS_TEXT = ["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#000000","#000000","#000000","#000000","#FFFFFF","#FFFFFF"]

DOWS = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI', 'DIMANCHE']

HOUR_PIXELS = 42

FMT_TIME = "%H:%M"
FMT_DATE = "%Y-%m-%d"
FMT_DATE_PRETTY = "%d/%m/%Y"
FMT_DATETIME = "%Y-%m-%d %H:%M"

ADV_LEVEL = (
    ('0', 'Débutants'),
    ('1', 'Tranquille'),
    ('2', 'Intermédiaire'),
    ('3', 'Difficile'),
    ('4', 'Chevronnés'),
)
