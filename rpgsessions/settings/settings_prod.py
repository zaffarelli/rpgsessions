from pathlib import Path
import os

SECRET_KEY = '^ghph5x=x*u+x6(^2y7p-is6zv)lkia0(+@74x076p0ot4ic+z'
DEBUG = False
ALLOWED_HOSTS = ['senestre.eu']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'extradb',
        'USER': 'fernando',
        'PASSWORD': 'casabuentes',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': None,
        },
}

STATIC_ROOT = '/srv/rpgsessions_static/'
MEDIA_ROOT = '/srv/rpgsessions_media/'


LOGPATH = os.path.join(BASE_DIR, 'logs/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(message)s",
            'datefmt': "%d:%H%M%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGPATH + "rpgsessions.log",
            'maxBytes': 1000000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'collector': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST_USER = "fernando.casabuentes@gmail.com"
EMAIL_HOST_PASSWORD = "fqyozcbjwflhmmlp"
