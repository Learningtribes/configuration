import requests

url = "https://devops-dashboard.triboolearning.com/api/downtimelog"
headers = {'Authorization': 'token'}

r_access_token = 'token'
r_headers = {'Authorization': 'Key '+r_access_token}

entities_response = requests.get('http://127.0.0.1:8082/api/core/v2/namespaces/default/entities', headers = r_headers)
#print entities_response.status_code
for i in entities_response.json():
    instance_name = i['metadata']['name']
    event_response = requests.get('http://127.0.0.1:8082/api/core/v2/namespaces/default/events/'+instance_name+'/keepalive', headers = r_headers)
    #print event_response.status_code
    instance_status = event_response.json()['check']['status']
    if instance_status != 0:
        a = requests.post(url, headers=headers, data={'client_hostname': instance_name, 'downtime_log': 'instance down'})