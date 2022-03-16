import boto3
import datetime
import time
import os

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
        Granularity = 'DAILY',
        Metrics = ['BlendedCost'],
        Filter = {'Tags': {'Key': 'cost-name', 'Values': [i]}}
    )
    cost=response_tag_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    if i == '':
        print 'No Tagged: '+str(cost)
    else:
        print str(i)+': '+str(cost)
        break
'''

response_ce_cost = client.get_cost_and_usage(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
    },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS Cost Explorer']}}
)
ce_cost = response_ce_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
print ce_cost
print float(ce_cost)
print round(float(ce_cost), 2)


response_waf_cost = client.get_cost_and_usage(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
    },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS WAF']}}
)
waf_cost = response_waf_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
print waf_cost
print float(waf_cost)
print round(float(waf_cost), 2)


response_ct_cost = client.get_cost_and_usage(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
    },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS CloudTrail']}}
)
ct_cost = response_ct_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
print ct_cost
print float(ct_cost)
print round(float(ct_cost), 2)


response_cw_cost = client.get_cost_and_usage(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
    },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': ['AmazonCloudWatch']}}
)
cw_cost = response_cw_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
print cw_cost
print float(cw_cost)
print round(float(cw_cost), 2)


response_kms_cost = client.get_cost_and_usage(
    TimePeriod = {
        'Start': start_day,
        'End': end_day
    },
    Granularity = 'MONTHLY',
    Metrics = ['BlendedCost'],
    Filter = {'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS Key Management Service']}}
)
kms_cost = response_kms_cost['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
print kms_cost
print float(kms_cost)
print round(float(kms_cost), 2)


