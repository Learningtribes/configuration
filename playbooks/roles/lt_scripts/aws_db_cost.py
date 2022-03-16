import boto3
import datetime
import os
import mysql.connector
from pymongo import MongoClient

'''
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

client = boto3.client('ce', region_name='us-east-1')
'''

mydb = mysql.connector.connect(host='localhost', user='root', password='A_uiLkq,u2d#')

cursor = mydb.cursor()
select_query = "SELECT table_schema AS 'DB_Name', ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS 'DB_Size_in_MB' FROM information_schema.tables GROUP BY table_schema ORDER BY SUM(data_length + index_length) DESC;"
cursor.execute(select_query)
for i in cursor.fetchall():
    print i






mongodb = MongoClient('mongodb://lt-readonly:password@127.0.0.1')

for i in mongodb.list_databases():
    print i
