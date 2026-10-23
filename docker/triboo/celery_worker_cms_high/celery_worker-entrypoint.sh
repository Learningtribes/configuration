#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py cms --settings=aws celery worker --loglevel=info --queues=edx.cms.core.high --hostname=edx.cms.core.high.%h --concurrency=1 --heartbeat-interval=120