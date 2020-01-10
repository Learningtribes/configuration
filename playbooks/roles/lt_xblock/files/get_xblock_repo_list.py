import requests
import os

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']


payload = {'per_page': '999'}
r = requests.get('https://api.github.com/orgs/Learningtribes/repos', auth=(username, password), params=payload)

for i in r.json():
    if 'xblock' in i['name'].lower():
        print i['name']
