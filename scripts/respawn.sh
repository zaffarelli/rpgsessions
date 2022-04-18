#!/usr/bin/env bash

rm ./rpgsessions/settings/settings.py
cp ./rpgsessions/settings/settings_prod.py ./rpgsessions/settings/settings.py
python ./manage.py migrate
python ./manage.py collectstatic --no-input
./scripts/super.sh restart gunicorn