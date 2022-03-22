#!/bin/bash

python scripts/gen_django_secret_key.py
python scripts/nginx_template_to_conf.py