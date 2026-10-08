#!/usr/bin/env bash
set -e

if [ -f /edx/app/xqueue/xqueue_env ]; then
    source /edx/app/xqueue/xqueue_env
fi


exec django-admin.py run_consumer --pythonpath=/edx/app/xqueue/xqueue --settings=xqueue.production