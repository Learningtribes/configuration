#!/bin/bash
set -e

if [ -f /edx/app/veda/veda_env ]; then
    source /edx/app/veda/veda_env
fi

exec gunicorn -c /edx/app/veda/veda_gunicorn.py VEDA.wsgi:application --access-logfile /var/log/veda/access.log --error-logfile /var/log/veda/error.log --log-level info