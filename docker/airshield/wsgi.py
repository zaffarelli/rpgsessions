import locale
import os
import sys
from django.core.wsgi import get_wsgi_application

# Apparently a fix is needed
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
locale.setlocale(locale.LC_ALL, 'C.UTF-8')

# DJANGO_WSGI: Better let that one off to track its usage (cve-aggregation/airshield/urls.py)
os.environ['DJANGO_WSGI'] = "true"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airshield.settings")

application = get_wsgi_application()
