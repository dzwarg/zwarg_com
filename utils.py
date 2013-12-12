from boto import ec2, rds

def get_ec2_hosts():
    conn = ec2.connect_to_region('us-east-1')
    return map(lambda x: x.public_dns_name, conn.get_only_instances())

def get_rds_host():
    conn = rds.connect_to_region('us-east-1')
    return map(lambda x: x.endpoint, conn.get_all_dbinstances())[0]
