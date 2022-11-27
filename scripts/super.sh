#!/usr/bin/env bash

set -e
supervisorctl -c ~/server_config/supervisord.conf $@