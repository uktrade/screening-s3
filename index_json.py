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
import boto3
today = datetime.now()
days_in_this_mount = calendar.monthrange(today.year, today.month)
proportion_to_the_mounth = days_in_this_mount[1]/today.day



class report_upload:
    def __init__(self):
        self.msg = ''
        self.today = datetime.now()


    def list_of_domins(self,user_id, user_pass):
        aws_client = boto3.client('cloudfront',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        return_index = {}
        return_index = aws_client.list_distributions()
        return (return_index)

    def route53_scean(self,user_id,user_pass):
        aws_client = boto3.client('route53',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        return_index = aws_client.list_hosted_zones()
        return (return_index)

    def acm_scean(self,user_id,user_pass):
        aws_client = boto3.client('acm',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        return_index  = aws_client.list_certificates()
        return(return_index)

    def location_s3_object_lookup(self,user_id,user_pass):
        aws_client = boto3.client('s3',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        s3_list = aws_client.list_buckets()
        #print (s3_list)
        return_index = {}
        for bucket in s3_list['Buckets']:
            return_index[bucket['Name'] + '_bucket'] = bucket
            return_index[bucket['Name']] =  aws_client.list_objects(Bucket=bucket['Name'])
        return(return_index)


    def ec2_zone_check(self,user_id,user_pass):
        aws_client = boto3.client('ec2',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        availability_zones = aws_client.describe_instances()
        return_index = {}
        return_index = availability_zones
        return (return_index)


if __name__ == '__main__':
    error_colector = report_upload()
    index= {}
    index['s3'] = []
    index['ec2'] = []
    index['cloudfront'] = []
    index['route53'] = []
    index['acm'] = []
    for user in os.environ:
        if user.startswith('AKI'):
            index['ec2'].append(error_colector.ec2_zone_check(user, os.environ[user]))
            index['s3'].append(error_colector.location_s3_object_lookup(user, os.environ[user]))
            index['cloudfront'].append(error_colector.list_of_domins(user, os.environ[user]))
            index['route53'].append(error_colector.route53_scean(user, os.environ[user]))
            index['acm'].append(error_colector.acm_scean(user, os.environ[user]))
    print(index)
