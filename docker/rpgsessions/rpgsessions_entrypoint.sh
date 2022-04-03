#!/usr/bin/env bash

# Todo: As a global note:
# rpgsessions-admin <=> python ./manage.py
# to be fixed later (Friedel uses symlink to handle that in RPM)

python ./manage.py migrate
#python ./manage.py createcachetable
chown -R www-data:www-data /srv
chmod -R 755 /srv
python ./manage.py collectstatic --no-input
python ./manage.py shell < create_rpgsessions_superuser.py
#python ./manage.py stats

#cd /usr/local/bin/

#./celery_start.sh
#echo "Celery started"

#airshield-admin fetch_normalize_legacy_nvd

gunicorn -b 0.0.0.0:8080 rpgsessions.wsgi

