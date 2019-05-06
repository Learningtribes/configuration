#!/bin/bash

while (ps auxf |grep '/bin/sh /usr/lib/apt/apt.systemd.daily install' |grep -v 'grep')
do
  sleep 30
done
