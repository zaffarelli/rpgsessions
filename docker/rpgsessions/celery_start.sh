#!/bin/bash
mkdir -p /var/run/celery
chown -R www-data:www-data /var/run/celery
chmod -R 777 /var/run/celery
chown -R www-data:www-data /var/log/airshield/
chmod -R 777 /var/log/airshield


#service /usr/local/bin/celeryd start
#service /usr/local/bin/celerybeat start


celery -A airshield amqp
celery -A airshield multi start 9 -A airshield -l debug -c2 --pidfile=/var/run/celery/airshield_celery_%n.pid --logfile=/var/log/airshield/airshield_celery.log
# -B -E -O fair
# -Q celery,post,files,fetch,cpe
#celery status
celery -A airshield control add_consumer celery
celery -A airshield control add_consumer post
celery -A airshield control add_consumer files
celery -A airshield control add_consumer fetch
celery -A airshield control add_consumer cpe

celery -A airshield beat --detach --pidfile=/var/run/celery/airshield_beat.pid --logfile=/var/log/airshield/airshield.log --schedule=/var/run/celery/celerybeat-schedule

