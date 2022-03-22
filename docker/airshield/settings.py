from .settings_global import *  # DO NOT remove this line under any circumstances!
import hashlib
import os
from pathlib import Path


# Get secrets from files
def env_from_file(tag, envvar, fallback):
    try:
        with open('/run/secrets/%s' % tag) as f:
            os.environ[envvar] = f.read().strip()
    except FileNotFoundError:
        os.environ[envvar] = os.getenv(envvar, fallback)


# Working around the ENVVAR_FILE stuff to get ENVVAR from the file directly, from EF's Noxcrux
env_from_file("airshield_db_password", "DB_PASSWORD", "something")
env_from_file("django_secret", "DJANGO_SECRET", "something")

BASE_DIR = Path(__file__).resolve()
SRV_DIR = os.environ.get("SRV_DIR", "/")
# Workaround tricky readings of booleans as environment variables
DEBUG = os.environ.get('DEBUG', "false").lower() in ["true", "1", "t", "on", "yes", "y", "ok"]

TIME_ZONE = 'Europe/Paris'

AIRSHIELD_SOURCES = {
    'NVD: JSON 1.1': {
        'type': 'NVDJsonFetcher',
        'urlbase': 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-'
    },
    'RedHat': {
        'type': 'RedHatFetcher',
        'url': 'https://www.redhat.com/security/data/metrics/rhsamapcpe.txt'},
    'Vilocify: JSON 1.0': {
        'type': 'VilocifyJsonFetcher',
        'urlbase': 'https://api.vilocify.com/v1/',
        'client_cert': '/etc/saml/certs/odysseus_cert.pem',
        'client_key': '/etc/saml/certs/odysseus_key.pem',
        'client_key_passphrase': None
    },
    'AirShieldDump': {
        'type': 'AirShieldDumpImporter',
        'path': '/srv/incoming/',
        'check_hash': True
    },
}

# Not sure why this one is here instead of being in settings_globals
AIRSHIELD_INCREMENTAL_DUMP_DAYS = 8

# This Airshield is not OTRS connected:
AIRSHIELD_SOAP = {
}

# Add your address in the ("Alex", "<email>") format to be flooded by Airshield...
ADMINS = []
MANAGERS = ADMINS
EMAIL_HOSTS = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# This is a replacement of whatever has already be set up, so I redeclare the important CONN_MAX_AGE param (May 2021
# issue):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', "wrong_host"),
        'PORT': 5432,
        'CONN_MAX_AGE': None,
    },
}

STATIC_ROOT = '%s/airshield_static/' % SRV_DIR
MEDIA_ROOT = '%s/airshield_media/' % SRV_DIR

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '127.0.0.1')]
# Rebuilt in pre-up.sh if needed:
SECRET_KEY = os.environ.get('DJANGO_SECRET')

# Careful, this is an add on, not a replacement:
AUTHENTICATION_BACKENDS += (  # noqa
    'django.contrib.auth.backends.ModelBackend',  # this is default'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.environ.get('AIRSHIELD_LOG'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

from celery.schedules import crontab

AIRSHIELD_CVE_AGGREGATION_SCHEDULE = crontab(minute='0,20,40')

CELERY_RESULT_BACKEND = 'redis://' + os.environ.get('REDIS_BACKEND', 'nohost') + '?new_join=1'
BROKER_URL = 'amqp://@%s' % (os.environ.get('RABBIT_BROKER', 'nohost'))
