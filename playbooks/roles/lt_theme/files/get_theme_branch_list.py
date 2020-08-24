import requests
import os

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']

branches_list = []
page_num = 1
i = 20
while i < 30:
    payload = {'per_page': '100', 'page': page_num}
    print payload
    r = requests.get('https://api.github.com/repos/Learningtribes/triboo-theme/branches', auth=(username, password), params=payload)
    for j in r.json():
        branches_list.append(j['name'])
    branches_num = len(r.json())
    if branches_num == 100:
        page_num += 1
        print page_num
    else:
        i = 30


for i in branches_list:
    print i