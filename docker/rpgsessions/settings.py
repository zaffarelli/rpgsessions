from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve()
SRV_DIR = os.environ.get("SRV_DIR", "/")
# # Workaround tricky readings of booleans as environment variables
DEBUG = os.environ.get('DEBUG', "false").lower() in ["true", "1", "t", "on", "yes", "y", "ok"]
# BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '^ghph5x=x*u+x6(^2y7p-is6zv)lkia0(+@74x076p0ot4ic*-'

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '127.0.0.1')]

INSTALLED_APPS = [
    'scheduler.apps.SchedulerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'fixture_magic',
    'colorfield',
    'fontawesomefree',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

ROOT_URLCONF = 'rpgsessions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scheduler.context_processors.commons',
            ],
        },
    },
]

WSGI_APPLICATION = 'rpgsessions.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
DATETIME_FORMAT = "D Y/m/d H:i"
DATE_FORMAT = "D Y/m/d"
TIME_FORMAT = "H:i"
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = 'rpgsessions_static/'
MEDIA_ROOT = 'rpgsessions_media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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

VERSION = "0.7.0"



# from .settings_global import *  # DO NOT remove this line under any circumstances!
# import hashlib
# import os
# from pathlib import Path
#
#
# # Get secrets from files
# def env_from_file(tag, envvar, fallback):
#     try:
#         with open('/run/secrets/%s' % tag) as f:
#             os.environ[envvar] = f.read().strip()
#     except FileNotFoundError:
#         os.environ[envvar] = os.getenv(envvar, fallback)
#
#
# # Working around the ENVVAR_FILE stuff to get ENVVAR from the file directly, from EF's Noxcrux
# env_from_file("airshield_db_password", "DB_PASSWORD", "something")
# env_from_file("django_secret", "DJANGO_SECRET", "something")
#
# BASE_DIR = Path(__file__).resolve()
# SRV_DIR = os.environ.get("SRV_DIR", "/")
# # Workaround tricky readings of booleans as environment variables
# DEBUG = os.environ.get('DEBUG', "false").lower() in ["true", "1", "t", "on", "yes", "y", "ok"]
#
# TIME_ZONE = 'Europe/Paris'
#
# AIRSHIELD_SOURCES = {
#     'NVD: JSON 1.1': {
#         'type': 'NVDJsonFetcher',
#         'urlbase': 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-'
#     },
#     'RedHat': {
#         'type': 'RedHatFetcher',
#         'url': 'https://www.redhat.com/security/data/metrics/rhsamapcpe.txt'},
#     'Vilocify: JSON 1.0': {
#         'type': 'VilocifyJsonFetcher',
#         'urlbase': 'https://api.vilocify.com/v1/',
#         'client_cert': '/etc/saml/certs/odysseus_cert.pem',
#         'client_key': '/etc/saml/certs/odysseus_key.pem',
#         'client_key_passphrase': None
#     },
#     'AirShieldDump': {
#         'type': 'AirShieldDumpImporter',
#         'path': '/srv/incoming/',
#         'check_hash': True
#     },
# }
#
# # Not sure why this one is here instead of being in settings_globals
# AIRSHIELD_INCREMENTAL_DUMP_DAYS = 8
#
# # This Airshield is not OTRS connected:
# AIRSHIELD_SOAP = {
# }
#
# # Add your address in the ("Alex", "<email>") format to be flooded by Airshield...
# ADMINS = []
# MANAGERS = ADMINS
# EMAIL_HOSTS = 'localhost'
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
#
# # This is a replacement of whatever has already be set up, so I redeclare the important CONN_MAX_AGE param (May 2021
# # issue):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST', "wrong_host"),
#         'PORT': 5432,
#         'CONN_MAX_AGE': None,
#     },
# }
#
# STATIC_ROOT = '%s/airshield_static/' % SRV_DIR
# MEDIA_ROOT = '%s/airshield_media/' % SRV_DIR
#
# ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '127.0.0.1')]
# # Rebuilt in pre-up.sh if needed:
# SECRET_KEY = os.environ.get('DJANGO_SECRET')
#
# # Careful, this is an add on, not a replacement:
# AUTHENTICATION_BACKENDS += (  # noqa
#     'django.contrib.auth.backends.ModelBackend',  # this is default'
# )
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.environ.get('AIRSHIELD_LOG'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
#
# from celery.schedules import crontab
#
# AIRSHIELD_CVE_AGGREGATION_SCHEDULE = crontab(minute='0,20,40')
#
# CELERY_RESULT_BACKEND = 'redis://' + os.environ.get('REDIS_BACKEND', 'nohost') + '?new_join=1'
# BROKER_URL = 'amqp://@%s' % (os.environ.get('RABBIT_BROKER', 'nohost'))
