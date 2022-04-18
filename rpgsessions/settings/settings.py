SECRET_KEY = '^ghph5x=x*u+x6(^2y7p-is6zv)lkia0(+@74x076p0ot4ic*-'
DEBUG = True
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'extraventures',
        'USER': 'extraventures',
        'PASSWORD': 'extraventures',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': None,
        },
}


STATIC_ROOT = 'rpgsessions_static/'
MEDIA_ROOT = 'rpgsessions_media/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST_USER = "fernando.casabuentes@gmail.com"
EMAIL_HOST_PASSWORD = "fqyozcbjwflhmmlp"


LOGPATH = os.path.join(BASE_DIR, 'logs/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(message)s",
            'datefmt': "%Y-%m-%d"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGPATH+"/rpgsessions.log",
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


VERSION = "(DEV)"+VERSION