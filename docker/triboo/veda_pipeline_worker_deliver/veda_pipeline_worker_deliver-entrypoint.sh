#!/usr/bin/env bash
set -e

if [ -f /edx/app/veda_pipeline_worker/veda_pipeline_worker_env ]; then
    source /edx/app/veda_pipeline_worker/veda_pipeline_worker_env
fi

exec python /edx/app/veda_pipeline_worker/veda_pipeline_worker/bin/deliver