import requests
import os

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']

r = requests.get('https://api.github.com/repos/Learningtribes/triboo-theme/branches', auth=(username, password))

branch_list = []
for i in r.json():
    branch_list.append(i['name'])

print branch_list