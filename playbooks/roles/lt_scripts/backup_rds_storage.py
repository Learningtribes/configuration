import boto3
import datetime
#import time
import botocore
import pytz


string_prod_db = 'platform-rds-cluster'


rds_eu_ie = boto3.client('rds', region_name='eu-west-1')
rds_eu_ie_string = 'eu-west-1'
rds_eu_se = boto3.client('rds', region_name='eu-north-1')
rds_eu_se_rds_key = 'e7f372e2-01a6-479b-9b6b-7b2dad74c199'

rds_us_east = boto3.client('rds', region_name='us-east-1')
rds_us_east_string = 'us-east-1'
rds_us_west = boto3.client('rds', region_name='us-west-2')
rds_us_west_rds_key = '17afd1f1-4eb4-4909-b4fb-824e71503a0a'

rds_cn_bj = boto3.client('rds', region_name='cn-north-1')
rds_cn_bj_string = 'cn-north-1'
rds_cn_nx = boto3.client('rds', region_name='cn-northwest-1')

snapshot_tag = [
    {'Key': 'cost-name', 'Value': 'GLOBAL-TRIBOO-SHARED-PRODUCTION-DB'},
    {'Key': 'cost-center', 'Value': 'GLOBAL'},
    {'Key': 'product', 'Value': 'TRIBOO'},
    {'Key': 'client', 'Value': 'SHARED'},
    {'Key': 'resource-type', 'Value': 'PRODUCTION'},
    {'Key': 'resource-name', 'Value': 'DB'},
    {'Key': 'db-type', 'Value': 'MYSQL'},
]



def copy_snapshot_job(region, dest_region, source_region_string, dest_region_rds_key, region_tag):
    response_describe_snapshot = region.describe_db_cluster_snapshots(
        DBClusterIdentifier=string_prod_db,
        SnapshotType='automated'
        )
    if response_describe_snapshot['DBClusterSnapshots']:
        for i in response_describe_snapshot['DBClusterSnapshots']:
            if i['SnapshotCreateTime'] > (datetime.datetime.now() - datetime.timedelta(1)).replace(tzinfo=pytz.timezone('UTC')):
                add_tags_on_automated_snapshot(region, i['DBClusterSnapshotArn'], region_tag)
                copy_snapshot_tag = snapshot_tag[:]
                copy_snapshot_tag.append({'Key': 'region', 'Value': region_tag})
                response_copy_snapshot = dest_region.copy_db_cluster_snapshot(
                    SourceDBClusterSnapshotIdentifier=i['DBClusterSnapshotArn'],
                    TargetDBClusterSnapshotIdentifier=i['DBClusterSnapshotIdentifier'].replace(':', '-'),
                    SourceRegion=source_region_string,
                    KmsKeyId=dest_region_rds_key,
                    Tags=copy_snapshot_tag
                    )
                print response_copy_snapshot

def add_tags_on_automated_snapshot(region, snapshot_string, region_tag):
    region_snapshot_tag = snapshot_tag[:]
    region_snapshot_tag.append({'Key': 'region', 'Value': region_tag})
    response_tag_snapshot = region.add_tags_to_resource(ResourceName=snapshot_string, Tags=region_snapshot_tag)
    print response_tag_snapshot


def delete_remote_old_snapshot_job(region, keep_day=15):
    expire_date = (datetime.datetime.now() - datetime.timedelta(days=keep_day)).replace(tzinfo=pytz.timezone('UTC'))
    response_describe_snapshot = region.describe_db_cluster_snapshots(SnapshotType='manual')
    if response_describe_snapshot['DBClusterSnapshots']:
        for j in response_describe_snapshot['DBClusterSnapshots']:
            if j['SnapshotCreateTime'] < expire_date:
                response_delete_snapshot = region.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier=j['DBClusterSnapshotIdentifier'])
                print response_delete_snapshot


copy_snapshot_job(rds_eu_ie, rds_eu_se, rds_eu_ie_string, rds_eu_se_rds_key, 'EU')
delete_remote_old_snapshot_job(rds_eu_se, 15)

copy_snapshot_job(rds_us_east, rds_us_west, rds_us_east_string, rds_us_west_rds_key, 'US')
delete_remote_old_snapshot_job(rds_us_west, 15)