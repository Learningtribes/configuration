#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py lms --settings=aws celery worker --loglevel=info --queues=edx.lms.core.grade --hostname=edx.lms.core.grade.%h --concurrency=10 --heartbeat-interval=120