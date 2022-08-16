import requests
import json
import datetime
import sys 


now_time = datetime.datetime.utcnow()
begin_time = now_time - datetime.timedelta(minutes=5)
begin_time = begin_time.strftime('%Y-%m-%dT%H:%M:%S')
end_time = now_time.strftime('%Y-%m-%dT%H:%M:%S')
now_time = now_time.strftime('%Y.%m.%d')

elastic_url = 'http://127.0.0.1:9200/filebeat-nginx-6.5.4-' + now_time + '/_search'
headers={'Content-Type': 'application/json'}
payload = {
            'aggs': {
              'hosts': {
                'terms': {'field': 'host.name.keyword', 'size': 200}
              }
            }
          }

r=requests.get(elastic_url, headers=headers, data=json.dumps(payload))
hosts_list=[]
r=r.json()
r=r['aggregations']['hosts']['buckets']
for i in r:
    hosts_list.append(i['key'])


warn_dict={}
crit_dict={}
exit_number=0
for host in hosts_list:
    payload2 = {
             'query': {
               'bool' : {
                 'must': [
                   {'match': {'nginx.access.response_code.keyword': '504'}},
                   {'match': {'host.name.keyword': host}},
                   {'range': {'@timestamp': {'gte': begin_time, 'lt': end_time}}},
                   {'range': {'nginx.access.request_time.keyword': {'gte': 50}}}
                 ]
               }
             },
             'size': 0
           }

    r2=requests.get(elastic_url, headers=headers, data=json.dumps(payload2))
    r2=r2.json()
    hit_number=r2['hits']['total']
    hit_number=int(hit_number)
    if hit_number >= 50:
        crit_dict[host] = hit_number
    elif hit_number >= 20:
        warn_dict[host] = hit_number

if warn_dict:
    exit_number=1
    for x,y in warn_dict.items():
        print 'Host: %s. Number of %s HTTP 504 occurred in 5 mins ago.' % (x, y)
if crit_dict:
    exit_number=2
    for x,y in crit_dict.items():
        print 'Host: %s. Number of %s HTTP 504 occurred in 5 mins ago.' % (x, y)
sys.exit(exit_number)