import requests
import os

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']

r = requests.get('https://api.github.com/repos/Learningtribes/triboo-theme/branches', auth=(username, password))


for i in r.json():
    print i['name']