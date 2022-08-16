import boto3
import datetime
import os
import requests



'''
current_day = datetime.date.today()
first_day_month = current_day - datetime.timedelta(days=current_day.day-1)
yesterday_day = (current_day - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

date_day = yesterday_day

if current_day == first_day_month:
    os._exit(0)

start_day = first_day_month.strftime("%Y-%m-%d")
end_day = current_day.strftime("%Y-%m-%d")
'''



current_day = datetime.date.today()
this_month_first_day = current_day.replace(day=1)
last_month_last_day = this_month_first_day - datetime.timedelta(days=1)
last_month_first_day = last_month_last_day.replace(day=1)
start_day = last_month_first_day.strftime("%Y-%m-%d")
end_day = this_month_first_day.strftime("%Y-%m-%d")
month = last_month_last_day.month
year = last_month_last_day.year
date_day = "%s-%s" % (year, month)



def insert_data(name, client_name, type, country, month, service_name, product, cost):
    url = 'https://devops-dashboard.triboolearning.com/api/awscost'
    payload = {'name': name, 'client_name': client_name, 'type': type, 'country': country, 'month': month, 'service_name': service_name, 'product': product, 'cost': cost}
    headers = {'Authorization': 'Token a5e3d87afc80a3848251919dc83303785a502063'}
    response = requests.request("POST", url, headers=headers, data = payload)
    print response.content

def get_service_cost(service_name):
    response_cost = client.get_cost_and_usage(
        TimePeriod = {
            'Start': start_day,
            'End': end_day
        },
        Granularity = 'MONTHLY',
        Metrics = ['BlendedCost'],
        Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': [service_name]}}
    )
    service_cost = response_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    return round(float(service_cost), 2)

def cost_add_tax(cost):
    cost = cost * 1.2
    return round(float(cost), 2)

client = boto3.client('ce', region_name='us-east-1')

response_tag = client.get_tags(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
        },
    TagKey='cost-name'
    )
tag_cost_list = response_tag['Tags']

for i in tag_cost_list:
    response_tag_cost = client.get_cost_and_usage(
        TimePeriod = {
                'Start': start_day,
                'End': end_day
                },
        Granularity = 'MONTHLY',
        Metrics = ['BlendedCost'],
        Filter = {'Tags': {'Key': 'cost-name', 'Values': [i]}}
    )
    cost=response_tag_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    if i == '':
        print 'No Tagged: '+str(cost)
    else:
        i_list = i.split('-')
        if '' in i_list:
            pass
        else:
            cost = round(float(cost), 2)
            cost = cost_add_tax(cost) 
            insert_data(('-').join(i.split('-')[0:4]), i_list[2], i_list[3], i_list[0], date_day, i_list[4], i_list[1], cost)
            break

cost_explorer_cost = get_service_cost('AWS Cost Explorer')
waf_cost = get_service_cost('AWS WAF')
cloudtrail_cost = get_service_cost('AWS CloudTrail')
cloudwatch_cost = get_service_cost('AmazonCloudWatch')
kms_cost = get_service_cost('AWS Key Management Service')

cost_explorer_cost = cost_add_tax(cost_explorer_cost)
waf_cost = cost_add_tax(waf_cost)
cloudtrail_cost = cost_add_tax(cloudtrail_cost)
cloudwatch_cost = cost_add_tax(cloudwatch_cost)
kms_cost = cost_add_tax(kms_cost)

insert_data('GLOBAL-TRIBOO-NO_CLIENT-BILLING', 'NO_CLIENT', 'BILLING', 'GLOBAL', date_day, 'API', 'TRIBOO', cost_explorer_cost)
insert_data('GLOBAL_EME-TRIBOO_2-SHARED-PRODUCTION', 'SHARED', 'PRODUCTION', 'GLOBAL_EME', date_day, 'ELB', 'TRIBOO_2', waf_cost)
insert_data('GLOBAL-TRIBOO-NO_CLIENT-TOOL', 'NO_CLIENT', 'TOOL', 'GLOBAL', date_day, 'CLOUDTRAIL', 'TRIBOO', cloudtrail_cost)
insert_data('GLOBAL-TRIBOO-NO_CLIENT-TOOL', 'NO_CLIENT', 'TOOL', 'GLOBAL', date_day, 'CLOUDWATCH', 'TRIBOO', cloudwatch_cost)
insert_data('GLOBAL-TRIBOO-NO_CLIENT-TOOL', 'NO_CLIENT', 'TOOL', 'GLOBAL', date_day, 'KMS', 'TRIBOO', kms_cost)


backup_intraflow_cost = client.get_cost_and_usage(
    TimePeriod = {
            'Start': start_day,
            'End': end_day
            },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'And': [{'Tags': {'Key': 'cost-name', 'MatchOptions': ['ABSENT']}}, {'Dimensions':{'Key': 'SERVICE', 'Values': ['EC2 - Other']}}] }
)
backup_intraflow_cost=backup_intraflow_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
backup_intraflow_cost = round(float(backup_intraflow_cost), 2)
backup_intraflow_cost = cost_add_tax(backup_intraflow_cost)
insert_data('GLOBAL-TRIBOO-SHARED-INTRAFLOW', 'SHARED', 'INTRAFLOW', 'GLOBAL', date_day, 'BACKUP', 'TRIBOO', backup_intraflow_cost)