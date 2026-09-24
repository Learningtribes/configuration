#!/usr/bin/env bash
set -e

if [ -f /edx/app/xqueue/xqueue_env ]; then
    source /edx/app/xqueue/xqueue_env
fi


exec gunicorn -c /edx/app/xqueue/xqueue_gunicorn.py  xqueue.wsgi --access-logfile /var/log/xqueue/access.log --error-logfile /var/log/xqueue/error.log --log-level info