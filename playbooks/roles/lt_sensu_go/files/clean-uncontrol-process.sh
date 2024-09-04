#!/bin/bash


function get_pid {
  PROCESS_ID=$(ps auxf | grep $1 | grep -v grep | awk '{print $2}')
  echo ${PROCESS_ID}
}

function in_main_id {
  CHECK_ID=$(pstree -ps $1 | grep $2)
}

function kill_id {
  kill -9 $1
}

function check_id {
  in_main_id $1 $2
  IN_RESULT=$?
  echo $1: ${IN_RESULT}
  if [ "${IN_RESULT}" -ne 0 ]
  then
    echo $1: kill
    kill_id $1
  fi
}

function clean_id {
  for i in $@
  do 
    check_id $i ${MAIN_PID}
  done
}


MAIN_PID=$(get_pid '/edx/app/supervisor/venvs/supervisor/bin/python')
L_PID=$(get_pid 'queues=edx.lms.core.leaderboard')
G_PID=$(get_pid 'queues=edx.lms.core.grade')

clean_id ${L_PID}
clean_id ${G_PID}