#!/bin/bash
timestamp=$(date +"%s")
hostname=$(hostname)

ps auxf |grep elastic |grep -v grep | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.elasticsearch", sum*1024, timestamp}'

ps auxf |grep cms_gunicorn.py |grep cms.wsgi | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.cms", sum*1024, timestamp}'

ps auxf |grep lms_gunicorn.py |grep lms.wsgi | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.lms", sum*1024, timestamp}'

ps auxf | grep nginx |grep worker | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.nginx", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'grade' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.grade", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'leaderboard' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.leaderboard", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'progress' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.progress", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'cms.core.low' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.cms_low", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'lms.core.high_mem' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.lms_high_mem", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'cms.core.high' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.cms_high", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'lms.core.default' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.lms_default", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'cms.core.default' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.cms_default", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'lms.core.low' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.lms_low", sum*1024, timestamp}'

ps auxf |grep  'aws celery worker' |grep 'lms.core.high' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.lms_high", sum*1024, timestamp}'

ps auxf |grep 'encode_worker' |grep 'veda' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.veda_encode", sum*1024, timestamp}'

ps auxf |grep 'veda_pipeline_worker' |egrep 'ingest|loop' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.veda_ingest", sum*1024, timestamp}'

ps auxf |grep 'veda_pipeline_worker' |grep 'deliver' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.worker.veda_deliver", sum*1024, timestamp}'

ps auxf |grep 'veda_gunicorn.py' |grep 'application' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.veda_web", sum*1024, timestamp}'

ps auxf | grep 'xqueue' |grep 'consumer' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.xqueue_consumer", sum*1024, timestamp}'

ps auxf | grep 'xqueue' |grep 'gunicorn' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.xqueue", sum*1024, timestamp}'

ps auxf |egrep 'unicorn.rb|forum'  | grep -v 'grep' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.forum", sum*1024, timestamp}'

ps auxf |grep 'certificate_agent.py' | grep -v 'grep' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memory.certs", sum*1024, timestamp}'

ps auxf | grep 'memcached' | awk '{print $2}' | xargs -i cat /proc/{}/smaps | awk -v timestamp=$timestamp -v hostname=$hostname '/Rss:/{ sum += $2 } END { print hostname".memcached.certs", sum*1024, timestamp}'