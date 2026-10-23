#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py lms --settings=aws celery worker --loglevel=info --queues=edx.lms.core.high_mem --hostname=edx.lms.core.high_mem.%h --concurrency=1 --heartbeat-interval=120 --maxtasksperchild 1