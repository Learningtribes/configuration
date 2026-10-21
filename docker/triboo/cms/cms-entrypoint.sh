#!/bin/bash
set -e

if [ -f /edx/app/edxapp/cms_env ]; then
    source /edx/app/edxapp/cms_env
fi

exec gunicorn -c /edx/app/edxapp/cms_gunicorn.py  cms.wsgi --access-logfile /var/log/cms/access.log --error-logfile /var/log/cms/error.log --log-level info