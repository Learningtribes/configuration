#!/bin/bash

if [ $(ps auxf |grep '\-Q encode_worker' | grep -v 'grep' | wc -l) -gt 2 ]
then
  /edx/bin/supervisorctl stop veda_encode_worker > /dev/null
  for i in $(ps ajxf |grep '\-Q encode_worker' | grep -v 'grep' | awk '{print -$3}' | uniq)
  do
    kill -9 $i
  done
  /edx/bin/supervisorctl start veda_encode_worker > /dev/null
else
  true
fi