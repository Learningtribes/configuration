#!/usr/bin/env bash

# This file is created and updated by ansible, edit at your peril



export PORT="8001"
export ADDRESS="127.0.0.1"
export LANG="en_US.UTF-8"
export DJANGO_SETTINGS_MODULE="lms.envs.aws"
export SERVICE_VARIANT="lms"
export PATH="/edx/app/edxapp/venvs/edxapp/bin:/edx/app/edxapp/edx-platform/bin:/edx/app/edxapp/edx-platform/node_modules/.bin:/edx/app/edxapp/nodeenvs/edxapp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export BOTO_CONFIG="/edx/app/edxapp/.boto"

source /edx/app/edxapp/edxapp_env
/edx/app/edxapp/venvs/edxapp/bin/gunicorn -c /edx/app/edxapp/api_extended_user_progress_report_gunicorn.py lms.wsgi