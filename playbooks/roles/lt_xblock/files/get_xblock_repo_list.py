import requests
import os

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']

r = requests.get('https://api.github.com/orgs/Learningtribes/repos', auth=(username, password))

for i in r.json():
    if 'xblock' in i['name'].lower():
        print i['name']
