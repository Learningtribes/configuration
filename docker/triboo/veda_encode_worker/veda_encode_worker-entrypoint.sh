#!/bin/bash
#--- Startup Script for VEDA Worker --#
set -e

if [ -f /edx/app/veda_encode_worker/veda_encode_worker_env ]; then
    source /edx/app/veda_encode_worker/veda_encode_worker_env
fi

echo "
* Video Worker *
"

#ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOTDIR=$PYTHONPATH
cd ${ROOTDIR}

# Get vars from yaml
QUEUE=$(cat ${ROOTDIR}/instance_config.yaml | grep celery_worker_queue)
QUEUE=${QUEUE#*: }
CONCUR=$(cat ${ROOTDIR}/instance_config.yaml | grep celery_threads)
CONCUR=${CONCUR#*: }
echo $QUEUE
echo $CONCUR

exec python ${ROOTDIR}/video_worker/celeryapp.py worker --loglevel=info --concurrency=${CONCUR} -Q ${QUEUE} -n worker.%h --without-gossip --without-mingle