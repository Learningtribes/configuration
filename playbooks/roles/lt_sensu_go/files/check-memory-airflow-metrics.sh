#!/bin/bash

getid ()
{
  ids=$(pgrep -P $1)
  if [ "$?" -eq 0 ]
  then
    for j in $ids
    do
      pid+=($j)
      getid $j
    done
  fi
}

pid=()
for i in $(ps auxf |grep ForkPoolWorker  |grep celeryd | awk '{print $2}')
do 
  pid+=($i)
  getid $i
done

memory=0
for x in ${pid[@]}
do 
  idmemory=$(cat /proc/$x/smaps | awk '/Rss:/{ sum += $2 } END { print sum}')
  memory=$(($memory+$idmemory))
done

memory=$(($memory*1024))
timestamp=$(date +"%s")
hostname=$(hostname)
echo "$hostname.memory.worker.airflow $memory $timestamp"