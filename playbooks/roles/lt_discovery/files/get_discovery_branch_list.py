import requests
import os



username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']

payload = {'per_page': '999'}
r = requests.get('https://api.github.com/repos/Learningtribes/course-discovery/branches', auth=(username, password), params=payload)


for i in r.json():
    print i['name']