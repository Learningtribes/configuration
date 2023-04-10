import requests

url = "https://devops-dashboard.triboolearning.com/api/downtimelog"
headers = {'Authorization': 'token'}

clients_response = requests.get('http://127.0.0.1:4567/clients')
#print clients_response.status_code
for i in clients_response.json():
    instance_name = i['name']
    result_response = requests.get('http://127.0.0.1:4567/results/'+instance_name+'/keepalive')
    #print result_response.status_code
    instance_status = result_response.json()['check']['status']
    if instance_status != 0:
        a = requests.post(url, headers=headers, data={'client_hostname': instance_name, 'downtime_log': 'instance down'})