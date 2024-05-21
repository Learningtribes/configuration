import boto3
import datetime
import pytz
import time


ec2_eu_ie = boto3.client('ec2', region_name='eu-west-1')
ec2_eu_ie_string = 'eu-west-1'
ec2_eu_se = boto3.client('ec2', region_name='eu-north-1')

ec2_us_east = boto3.client('ec2', region_name='us-east-1')
ec2_us_east_string = 'us-east-1'
ec2_us_west = boto3.client('ec2', region_name='us-west-2')

ec2_cn_bj = boto3.client('ec2', region_name='cn-north-1')
ec2_cn_bj_string = 'cn-north-1'
ec2_cn_nx = boto3.client('ec2', region_name='cn-northwest-1')


def check_snapshot_job(region, check_snapshot_list, job_limit=0):
    if job_limit == 0:
        for job in check_snapshot_list:
            response_snapshot = region.describe_snapshots(SnapshotIds=[job])
            if response_snapshot['Snapshots'][0]['State'] == 'completed':
                pass
            else:
                time.sleep(20)
                check_snapshot_job(region, check_snapshot_list)
        return
    else:
        if len(check_snapshot_list) == job_limit:
            pass
        else:
            return
        for job in check_snapshot_list:
            response_snapshot = region.describe_snapshots(SnapshotIds=[job])
            if response_snapshot['Snapshots'][0]['State'] == 'completed':
                check_snapshot_list.remove(job)
        time.sleep(20)
        check_snapshot_job(region, check_snapshot_list, job_limit)

def backup_volume_job(region):
    snapshot_list = []
    create_snapshot_list = []
    create_snapshot_date = datetime.date.today().strftime('%Y-%m-%d')
    response_volumes = region.describe_volumes(Filters=[{'Name':'tag:BACKUP', 'Values':['support']}])

    if response_volumes['Volumes']:
        for volume in response_volumes['Volumes']:
            if volume['State'] == 'in-use':
                if len(create_snapshot_list) == 4:
                    check_snapshot_job(region, create_snapshot_list, 4)
                snapshot_tags = volume['Tags']
                snapshot_tags.append({u'Key': 'backup-type', u'Value': 'hawthorn'})
                response_createsnapshot = region.create_snapshot(Description='snapshot from '+volume['VolumeId']+'('+volume['Attachments'][0]['InstanceId']+') at '+create_snapshot_date, VolumeId=volume['VolumeId'], TagSpecifications=[{'ResourceType':'snapshot', 'Tags': snapshot_tags}])
                print response_createsnapshot
                create_snapshot_list.append(response_createsnapshot['SnapshotId'])
                snapshot_list.append(response_createsnapshot['SnapshotId'])
        check_snapshot_job(region, snapshot_list)

def delete_local_old_snapshot_job(region, keep_day=10):
    response_snapshots = region.describe_snapshots(Filters=[{'Name': 'tag:backup-type', 'Values': ['hawthorn']}])
    if response_snapshots['Snapshots']:
        for snapshot in response_snapshots['Snapshots']:
            if snapshot['StartTime'] < pytz.UTC.localize(datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=keep_day), datetime.time.min)):
                response_delsnapshot = region.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print response_delsnapshot

def copy_snapshot_job(region, dest_region, source_region_string):
    snapshot_list = []
    copy_snapshot_list = []
    response_snapshots = region.describe_snapshots(Filters=[{'Name': 'tag:backup-type', 'Values': ['hawthorn']}])
    if response_snapshots['Snapshots']:
        for snapshot in response_snapshots['Snapshots']:
            if snapshot['StartTime'] > pytz.UTC.localize(datetime.datetime.combine(datetime.date.today(), datetime.time.min)):
                if len(copy_snapshot_list) == 4:
                    check_snapshot_job(dest_region, copy_snapshot_list, 4)
                response_copysnapshot = dest_region.copy_snapshot(Description=snapshot['Description'], SourceRegion=source_region_string, SourceSnapshotId=snapshot['SnapshotId'], Encrypted=True, TagSpecifications=[{'ResourceType':'snapshot', 'Tags': snapshot['Tags']}])
                print response_copysnapshot
                copy_snapshot_list.append(response_copysnapshot['SnapshotId'])
                snapshot_list.append(response_copysnapshot['SnapshotId'])
        check_snapshot_job(dest_region, snapshot_list)

def delete_remote_old_snapshot_job(region, keep_day=10):
    response_snapshots = region.describe_snapshots(OwnerIds=['419890668373'])
    if response_snapshots['Snapshots']:
        for snapshot in response_snapshots['Snapshots']:
            if snapshot['StartTime'] < pytz.UTC.localize(datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=keep_day), datetime.time.min)):
                response_delsnapshot = region.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print response_delsnapshot



backup_volume_job(ec2_eu_ie)
delete_local_old_snapshot_job(ec2_eu_ie, 10)
#copy_snapshot_job(ec2_eu_ie, ec2_eu_se, ec2_eu_ie_string)
delete_remote_old_snapshot_job(ec2_eu_se, 10)

backup_volume_job(ec2_us_east)
delete_local_old_snapshot_job(ec2_us_east, 10)
#copy_snapshot_job(ec2_us_east, ec2_us_west, ec2_us_east_string)
delete_remote_old_snapshot_job(ec2_us_west, 10)