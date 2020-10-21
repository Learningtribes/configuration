#!/bin/bash

monitor_lms_log_file='/edx/var/log/supervisor/lms-stderr.log'
monitor_cms_log_file='/edx/var/log/supervisor/cms-stderr.log'
lms_log_created_text='/opt/scripts/check_webpack_error_lms.txt' 
cms_log_created_text='/opt/scripts/check_webpack_error_cms.txt' 
lms_log_line_text='/opt/scripts/check_webpack_error_lms.2.txt'
cms_log_line_text='/opt/scripts/check_webpack_error_cms.2.txt'


function get_file_create_time
{
  monitor_file_name=$1
  file_inode=$(ls -i $monitor_file_name | cut -d' ' -f1)
  file_date=$(debugfs -R "stat <$file_inode>" /dev/nvme0n1p1 | grep 'crtime' | cut -d' ' -f 5-)
  echo $file_date 
}
#get_file_create_time $monitor_lms_log_file

function check_error
{
  monitor_file_name=$1
  log_line_text=$2
  error_exist=false
  
  if [ -f $log_line_text ]
  then
    last_line_number=$(cat $log_line_text)
    error_string=$(sed -n "$last_line_number,\$p" $monitor_file_name | grep 'WebpackLoaderBadStatsError' )
    if [ $? -eq 0 ]
    then
      error_exist=true
    fi
    new_last_line_number=$(wc -l $monitor_file_name | cut -d' ' -f1)
    echo $new_last_line_number > $log_line_text
  else
    error_string=$(sed -n '1,$p' $monitor_file_name | grep 'WebpackLoaderBadStatsError' )
    if [ $? -eq 0 ]
    then
      error_exist=true
    fi
    new_last_line_number=$(wc -l $monitor_file_name | cut -d' ' -f1)
    echo $new_last_line_number > $log_line_text
  fi
  if $error_exist
  then
    return 2
  fi
}
#check_error $monitor_lms_log_file $lms_log_line_text

function get_error_string
{
  monitor_file_name=$1
  log_create_text=$2
  log_line_text=$3
  error_exist=false

  if [ ! -f $log_create_text ]
  then
    get_file_create_time $monitor_file_name > $log_create_text
  fi

  get_file_date=$(cat $log_create_text)
  file_date=$(get_file_create_time $monitor_file_name)
  if [ "$get_file_date" = "$file_date" ]
  then
    check_error $monitor_file_name $log_line_text
    if [ $? -eq 2 ]
    then
      return 2
    fi
  else
    get_file_create_time $monitor_file_name > $log_create_text
    old_monitor_file_name=$(ls -lhrt $monitor_file_name* | tail -n 2 | head -n 1 | awk '{print $NF}')
    last_line_number=$(cat $log_line_text)
    error_string=$(sed -n "$last_line_number,\$p" $old_monitor_file_name | grep 'WebpackLoaderBadStatsError' )
    if [ $? -eq 0 ]
    then
      error_exist=true
    fi
    error_string=$(sed -n '1,$p' $monitor_file_name | grep 'WebpackLoaderBadStatsError' )
    if [ $? -eq 0 ]
    then
      error_exist=true
    fi
    new_last_line_number=$(wc -l $monitor_file_name | cut -d' ' -f1)
    echo $new_last_line_number > $log_line_text
    if $error_exist
    then
      return 2
    fi
  fi
}

lms_error_exist=false
cms_error_exist=false
get_error_string $monitor_lms_log_file $lms_log_created_text $lms_log_line_text
if [ $? -eq 2 ]
then
  lms_error_exist=true
fi
get_error_string $monitor_cms_log_file $cms_log_created_text $cms_log_line_text
if [ $? -eq 2 ]
then
  cms_error_exist=true
fi
if $lms_error_exist && $cms_error_exist
then
  echo 'LMS&CMS Webpack ERROR'
  exit 2
elif $lms_error_exist
then 
  echo 'LMS Webpack ERROR'
  exit 2
elif $cms_error_exist
then 
  echo 'CMS Webpack ERROR'
  exit 2
else
  echo 'Webpack health'
fi