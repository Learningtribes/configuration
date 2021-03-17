#!/bin/bash

commit_file=/root/platform.commit

function check_current_id {
  cd /edx/app/edxapp/edx-platform
  git log -n 1 | head -1 | awk '{print $2}'
}

if [ -f "$commit_file" ]; 
then
  true
else
  touch $commit_file
fi

current_string=$(grep 'current' $commit_file)
if [ "$?" -eq 0 ];
then
  file_current_id=$(echo $current_string | awk '{print $2}')
  current_id=$(check_current_id)
  if [ "$file_current_id" = "$current_id" ];
  then
    true
  else
    echo "current: $current_id" > $commit_file
    echo "previous: $file_current_id" >> $commit_file
  fi
else
  current_id=$(check_current_id)
  echo "current: $current_id" >> $commit_file
fi