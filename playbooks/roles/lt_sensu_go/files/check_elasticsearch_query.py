import requests
import sys

payload = {'from': 0, 'size': 10}
program_url = 'http://localhost:9200/program_index/_search'
courseware_url = 'http://localhost:9200/courseware_index/course_info/_search'

r1 = requests.get(program_url, params=payload, timeout=10)
r2 = requests.get(courseware_url, params=payload, timeout=10)

if r1.status_code != 200 or r2.status_code != 200:
    sys.exit(2)
else:
    sys.exit(0)