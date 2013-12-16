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

from storages.backends.s3boto import S3BotoStorage, S3BotoStorageFile


class S3BotoStorageSafe(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        return super(S3BotoStorageSafe, self).__init__(*args, **kwargs)

    def isfile(self, name):
        try:
            name = self._normalize_name(self._clean_name(name))
            f = S3BotoStorageFile(name, 'rb', self)
            if not f.key:
                return False
            return True
        except:
            return False

    def isdir(self, name):
        return not self.isfile(name)

    def move(self, old_file_name, new_file_name, allow_overwrite=False):

        if self.exists(new_file_name):
            if allow_overwrite:
                self.delete(new_file_name)
            else:
                raise "The destination file '%s' exists and allow_overwrite is False" % new_file_name

        old_key_name = self._encode_name(self._normalize_name(self._clean_name(old_file_name)))
        new_key_name = self._encode_name(self._normalize_name(self._clean_name(new_file_name)))

        k = self.bucket.copy_key(new_key_name, self.bucket.name, old_key_name)

        if not k:
            raise "Couldn't copy '%s' to '%s'" % (old_file_name, new_file_name)

        self.delete(old_file_name)

    def makedirs(self, name):
        # i can't create dirs still
        pass

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.list(self._encode_name(name))
        for item in dirlist:
            item.delete()

    def save(self, name, content):
        re = super(S3BotoStorageSafe, self).save(name, content)
        #key.copy(key.bucket, key.name, preserve_acl=True, metadata={'Content-Type': 'text/plain'})
        return re

StaticS3BotoStorage = lambda: S3BotoStorageSafe(location='static')
MediaS3BotoStorage = lambda: S3BotoStorageSafe(location='media') 