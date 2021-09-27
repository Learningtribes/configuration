#!/bin/bash

if /edx/bin/supervisorctl status veda_pipeline_worker_youtubecallback | grep STOPPED
then 
  true
else
  /edx/bin/supervisorctl stop veda_pipeline_worker_youtubecallback > /dev/null
fi

if [ $(ps auxf |grep 'veda_pipeline_worker/bin/loop.py' | grep -v 'grep' | wc -l) -gt 2 ]
then
  /edx/bin/supervisorctl stop veda_pipeline_worker_ingest > /dev/null
  for i in $(ps ajxf |grep 'veda_pipeline_worker/bin/loop.py' | grep -v 'grep' | awk '{print -$3}' | uniq)
  do
    kill -9 $i
  done
  /edx/bin/supervisorctl start veda_pipeline_worker_ingest > /dev/null
else
  true
fi