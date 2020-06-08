#!/bin/bash

if [ $(ps auxf |grep '\-Q deliver_worker' | grep -v 'grep' | wc -l) -gt 3 ]
then
  /edx/bin/supervisorctl stop veda_pipeline_worker_deliver > /dev/null
  for i in $(ps ajxf |grep '\-Q deliver_worker' | grep -v 'grep' | awk '{print -$3}' | uniq)
  do
    kill -9 $i
  done
  /edx/bin/supervisorctl start veda_pipeline_worker_deliver > /dev/null
else
  true
fi