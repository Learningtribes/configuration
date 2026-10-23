#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py lms --settings=aws celery worker --loglevel=info --queues=edx.lms.core.progress --hostname=edx.lms.core.progress.%h --concurrency=1 --heartbeat-interval=120 