import json
import requests
import os
import calendar
import operator
from datetime import datetime
import boto3
from math import trunc
import ssl
import socket
import threading
import boto3
import time
today = datetime.now()
days_in_this_mount = calendar.monthrange(today.year, today.month)
proportion_to_the_mounth = days_in_this_mount[1]/today.day



class aws_index:
    def __init__(self):
        self.msg = ''
        self.today = datetime.now()
        self.index = {}
        self.return_index = {}
        self.update_from_aws()

    def clean_index(self):
        self.index['s3'] = []
        self.index['ec2'] = []
        self.index['cloudfront'] = []
        self.index['route53'] = []
        self.index['acm'] = []


    def update_from_aws(self):
        self.clean_index()
        for user in os.environ:
            if user.startswith('AKI'):
                self.ec2_zone_check(user, os.environ[user])
                self.location_s3_object_lookup(user, os.environ[user])
                self.list_of_domins(user, os.environ[user])
                self.route53_scean(user, os.environ[user])
                self.acm_scean(user, os.environ[user])
        self.return_index = self.index

    def update_in_subpros_aws(self):
        background_aws_lookup = threading.Thread(target=self.update_from_aws)
        background_aws_lookup.start()

    def list_of_domins(self,user_id, user_pass):
        aws_client = boto3.client('cloudfront',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        self.index['cloudfront'].append(aws_client.list_distributions())

    def route53_scean(self,user_id,user_pass):
        aws_client = boto3.client('route53',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        self.index['route53'].append( aws_client.list_hosted_zones())


    def acm_scean(self,user_id,user_pass):
        aws_client = boto3.client('acm',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        self.index['acm'].append(aws_client.list_certificates())


    def location_s3_object_lookup(self,user_id,user_pass):
        aws_client = boto3.client('s3',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        s3_list = aws_client.list_buckets()
        return_index = {}
        for bucket in s3_list['Buckets']:
            return_index[bucket['Name'] + '_bucket'] = bucket
            return_index[bucket['Name']] =  aws_client.list_objects(Bucket=bucket['Name'])
        self.index['s3'].append(return_index)


    def ec2_zone_check(self,user_id,user_pass):
        aws_client = boto3.client('ec2',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        self.index['ec2'].append(aws_client.describe_instances())


if __name__ == '__main__':
    jo = aws_index()
    #jo.update_in_subpros_aws()
    print(jo.return_index)

