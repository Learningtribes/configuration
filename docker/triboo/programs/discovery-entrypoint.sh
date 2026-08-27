#!/usr/bin/env bash
set -e

if [ -f /edx/app/discovery/discovery_env ]; then
    source /edx/app/discovery/discovery_env
fi


exec gunicorn -c /edx/app/discovery/discovery_gunicorn.py  course_discovery.wsgi:application --access-logfile /var/log/discovery/access.log --error-logfile /var/log/discovery/error.log --log-level info