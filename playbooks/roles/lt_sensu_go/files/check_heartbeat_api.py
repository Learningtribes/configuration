import requests
import sys
import socket
import time

health_url = 'https://learning-tribes.com/heartbeat?extended'

error_list = []
request_timeout = False

try:
    response = requests.get(health_url, timeout=20)
    result = response.json()
    if not result['modulestore']['status']:
        error_list.append({'MongoDB': 'down'})
    if not result['sql']['status']:
        error_list.append({'MySQL': 'down'})
    if not result['elasticsearch']['status']:
        if result['elasticsearch']['message'] == 'timeout':
            error_list.append({'ElasticSearch': 'timeout'})
        else:
            error_list.append({'ElasticSearch': 'down'})
    if 'forum' in result:
        if not result['forum']['status']:
            error_list.append({'Forum': 'down'})
    if 'cache_set' in result:
        if not result['cache_set']['status']:
            error_list.append({'Memcachedb': 'down'})
    if 'cache_get' in result:
        if not result['cache_get']['status']:
            error_list.append({'Memcachedb': 'down'})
    if 'celery' in result:
        if not result['celery']['status']:
            if result['celery']['message'] == 'expired':
                error_list.append({'RabbitMQ': 'timeout'})
            else:
                error_list.append({'RabbitMQ': 'down'})
except requests.exceptions.Timeout:
    request_timeout = True


if request_timeout:
    print(socket.gethostname()+'.health.status 0 '+str(int(time.time())))
elif response.status_code != 200:
    print(socket.gethostname()+'.health.status 0 '+str(int(time.time())))
elif error_list != []:
    print(socket.gethostname()+'.health.status 0 '+str(int(time.time())))
else:
    print(socket.gethostname()+'.health.status 100 '+str(int(time.time())))


