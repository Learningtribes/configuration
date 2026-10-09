#!/usr/bin/env bash
set -e

if [ -f /edx/app/forum/forum_env ]; then
    source /edx/app/forum/forum_env
fi

if [ -f /edx/app/forum/forum_sensitive_env ]; then
    source /edx/app/forum/forum_sensitive_env
fi


exec /edx/app/forum/cs_comments_service/bin/unicorn -c config/unicorn_tcp.rb -I '.'