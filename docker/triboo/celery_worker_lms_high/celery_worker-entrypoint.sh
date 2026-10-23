#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py lms --settings=aws celery worker --pool=solo --loglevel=info --queues=edx.lms.core.high --hostname=edx.lms.core.high.%h