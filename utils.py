from boto import ec2, rds

class BotoConnection(object):
    """
    A connection to the Amazon EC2 and RDS services via boto.
    """

    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2_conn = ec2.connect_to_region(self.region)
        self.rds_conn = rds.connect_to_region(self.region)

    def get_ec2_hosts(self):
        return map(lambda x: x.public_dns_name, self.ec2_conn.get_only_instances())

    def get_rds_host(self):
        return map(lambda x: x.endpoint, self.rds_conn.get_all_dbinstances())[0][0]

    def get_rds_port(self):
        return map(lambda x: x.endpoint, self.rds_conn.get_all_dbinstances())[0][1]

    def get_rds_username(self):
        return map(lambda x: x.master_username, self.rds_conn.get_all_dbinstances())[0]

    def get_rds_dbname(self):
        return map(lambda x: x.DBName, self.rds_conn.get_all_dbinstances())[0]