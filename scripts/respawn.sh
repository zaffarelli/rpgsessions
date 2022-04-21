#!/usr/bin/env bash

cd ~/rpgsessions

sudo chown -R www-data:www-data /srv
sudo chmod -R a+w /srv

pip install -r requirements.txt

#git stash
#git fetch --all
#git pull

python ./manage.py migrate
python ./manage.py collectstatic --no-input
./scripts/super.sh restart gunicorn