import boto3
import datetime
import os
import mysql.connector
from pymongo import MongoClient


current_day = datetime.date.today()
first_day_month = current_day - datetime.timedelta(days=current_day.day-1)
yesterday_day = (current_day - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

print yesterday_day

if current_day == first_day_month:
    os._exit(0)

start_day = first_day_month.strftime("%Y-%m-%d")
end_day = current_day.strftime("%Y-%m-%d")
print start_day
print end_day

#client = boto3.client('ce', region_name='us-east-1')




mydb = mysql.connector.connect(host='localhost', user='root', password='A_uiLkq,u2d#')

cursor = mydb.cursor()
select_query = "SELECT table_schema AS 'DB_Name', ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS 'DB_Size_in_MB' FROM information_schema.tables GROUP BY table_schema ORDER BY SUM(data_length + index_length) DESC;"
cursor.execute(select_query)
total_size = 0
client_dict = {}
for i in cursor.fetchall():
    if i[0].startswith('learning-'):
        print i
        total_size = total_size + i[1]
        j = i[0].split('_')[0]
        if j not in client_dict.keys():
            client_dict[j] = i[1]
        else:
            client_dict[j] = client_dict[j] + i[1]
print total_size
print client_dict

for x,y in client_dict.items():
    print type(x), float(y)






mongodb = MongoClient('mongodb://lt-readonly:E2r8Tj8WRHJRrHEWTWRsnsKf@127.0.0.1')

total_size = 0
client_dict = {}
for i in mongodb.list_databases():
    if i['name'].startswith('learning-'):
        print i
        total_size = total_size + i['sizeOnDisk']
        j = i['name'].split('_')[0]
        if j not in client_dict.keys():
            client_dict[j] = i['sizeOnDisk']
        else:
            client_dict[j] = client_dict[j] + i['sizeOnDisk']
print total_size
print client_dict

for x,y in client_dict.items():
    print x, float(y)



