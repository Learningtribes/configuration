from ConfigParser import SafeConfigParser
import sys

hosts_file = sys.argv[1]
region = sys.argv[2]

region_setion = str(region) + ':children'

tenant_list = []
parser = SafeConfigParser(allow_no_value=True)
parser.read(hosts_file)

for i in parser.items(region_setion):
    if 'stateful' not in i[0]:
        tenant_name = i[0]
        single_tenant_string = tenant_name
        tenant_ip_list = parser.items(i[0])
        for j in tenant_ip_list:
            single_tenant_string = single_tenant_string + ',' + j[0]
        print single_tenant_string