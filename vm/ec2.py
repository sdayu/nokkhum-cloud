'''
Created on Jun 19, 2012

@author: boatkrap
'''
import time
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

    def get_image(self, image_id):
        return self.connection.get_image(image_id)

    def start_instance(self, image_id, instance_type='m1.small'):
        image = self.connection.get_image(image_id)
        reservation = image.run(instance_type=instance_type)
        instance = reservation.instances[0]
        instance.update()
        if instance.state != "running":
            time.sleep(0.5)
            instance.update()

        return instance

    def stop_instance(self, instance_id):
        instance = self.find_instance(instance_id)
        if instance:
            instance.stop()

    def reboot_instance(self, instance_id):
        instance = self.find_instance(instance_id)
        if instance:
            instance.reboot()

    def terminate_instance(self, instance_id):
        instance = self.find_instance(instance_id)
        if instance:
            instance.terminate()

    def find_instance(self, instance_id):
        reservations = self.connection.get_all_reservations()

        found_instance = None
        found = False
        for reservation in reservations:
            for instance in reservation.instances:
                if instance.id == instance_id:
                    found_instance = instance
                    found = True
                    break
            if found:
                break

        return found_instance

