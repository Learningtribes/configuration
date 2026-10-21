#!/bin/bash
set -e

if [ -f /edx/app/edxapp/lms_env ]; then
    source /edx/app/edxapp/lms_env
fi

exec gunicorn -c /edx/app/edxapp/lms_gunicorn.py lms.wsgi --access-logfile /var/log/lms/access.log --error-logfile /var/log/lms/error.log --log-level info