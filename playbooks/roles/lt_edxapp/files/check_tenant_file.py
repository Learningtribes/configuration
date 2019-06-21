from ConfigParser import SafeConfigParser
import sys
import boto3
import os
from git import Repo 



ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
GITHUB_USERNAME = os.environ['GITHUB_USERNAME']
GITHUB_PASSWORD = os.environ['GITHUB_PASSWORD']


repo_path = sys.argv[1]
region = sys.argv[2]
credential_file = sys.argv[3]

hosts_file = repo_path + '/hosts.ini'
region_setion = str(region) + ':children'

parser = SafeConfigParser(allow_no_value=True)
parser.optionxform = str
parser.read(hosts_file)


file_hosts_dict = {}
for i in parser.items(region_setion):
    if 'stateful' not in i[0]:
        tenant_name = i[0]
        new_tenant_ip_list = []
        tenant_ip_list = parser.items(tenant_name)
        for j in tenant_ip_list:
            new_tenant_ip_list.append(j[0])
        file_hosts_dict[tenant_name] = new_tenant_ip_list

new_host_dict = {}
client = boto3.client('ec2', region_name=region, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
for i in file_hosts_dict.keys():
    real_ip_list = []
    tenant_name = i
    tenant_ip_list = file_hosts_dict[tenant_name]
    tenant_ip_list.sort()
    instance_name = 'Platform APP ' + i.replace('_tenant','')
    response = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
    if len(response['Reservations']) == 0:
        remove_folder = repo_path + '/group_vars/' + tenant_name
        shutil.rmtree(remove_folder)
        parser.remove_section(tenant_name)
        parser.remove_option(region_setion, tenant_name)
        parser.remove_option('tenants:children', tenant_name)
        fp = open(hosts_file,'w')
        parser.write(fp)
        fp.close()
        repo = Repo(repo_path)
        with repo.git.custom_environment(GIT_USERNAME=GITHUB_USERNAME, GIT_PASSWORD=GITHUB_PASSWORD):
            repo.git.config('credential.helper', '/bin/bash ' + credential_file)
            repo.git.branch('--set-upstream-to=origin/master', 'master')
            repo.git.add('-A')
            repo.git.commit('-m', 'remove ' + tenant_name)
            repo.git.push()
            repo.git.config('--remove-section', 'credential')
    else:
        for j in response['Reservations'][0]['Instances']:
            real_ip_list.append(j['PublicIpAddress'])   
        real_ip_list.sort()
        if tenant_ip_list == real_ip_list:
            pass
        else:
            new_host_dict[tenant_name] = real_ip_list
            if len(new_host_dict.values()[0]) != 0:
                parser.remove_section(tenant_name)
                parser.add_section(tenant_name)
                for g in new_host_dict.values()[0]:
                    parser.set(tenant_name, g)
            fp = open(hosts_file,'w')
            parser.write(fp)
            fp.close()
            repo = Repo(repo_path)
            with repo.git.custom_environment(GIT_USERNAME=GITHUB_USERNAME, GIT_PASSWORD=GITHUB_PASSWORD):
                repo.git.config('credential.helper', '/bin/bash ' + credential_file)
                repo.git.branch('--set-upstream-to=origin/master', 'master')
                repo.git.add('hosts.ini')
                repo.git.commit('-m', '"modify ' + tenant_name + ' IP: ' + str(real_ip_list) + '"')
                repo.git.push()
                repo.git.config('--remove-section', 'credential')

