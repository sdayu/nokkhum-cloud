'''
Created on Jun 19, 2012

@author: boatkrap
'''

import boto.ec2.connection
from boto.ec2 import regioninfo

class EC2Client:

    def __init__(self, access_key_id, secret_access_key, host, port, secure=False, region_name="RegionOne", path='/services/Cloud'):
        self.connection = boto.ec2.connection.EC2Connection(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            port=port,
            region=regioninfo.RegionInfo(name=region_name, endpoint=host),
            host=host,
            is_secure=secure,
            path=path,
            debug=2
        )
        
    def get_all_images(self):
        return self.connection.get_all_images()
    
    def get_all_instances(self):
        return self.connection.get_all_instances()
