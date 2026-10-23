#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py lms --settings=aws celery worker --loglevel=info --queues=edx.lms.core.default --hostname=edx.lms.core.default.%h --concurrency=1 --heartbeat-interval=120 