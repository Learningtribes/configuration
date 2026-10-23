#!/usr/bin/env bash
set -e

exec python /edx/app/edxapp/edx-platform/manage.py cms --settings=aws celery worker --loglevel=info --queues=edx.cms.core.low --hostname=edx.cms.core.low.%h --concurrency=1 --heartbeat-interval=120 