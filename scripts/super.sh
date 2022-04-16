#!/usr/bin/env bash

set -e
supervisorctl -c config/supervisord.conf $@