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
        url_list = []
        list_cfront = aws_client.list_distributions()
        if not 'Items' in list_cfront['DistributionList']:
            list_cfront['DistributionList'] = {}
            list_cfront['DistributionList']['Items'] = []
        for clfront in list_cfront['DistributionList']['Items']:
            try:
                for url_name in clfront['Aliases']["Items"]:
                    url_list.append(url_name)
            except:
                self.msg = self.msg + ("\n cloudFront whith out Alias " + clfront['Id'] + " used this TargetOriginId " + clfront['DefaultCacheBehavior']['TargetOriginId'])
                pass
        #return (url_list)



    def location_s3_object_lookup(self,user_id,user_pass):
        aws_client = boto3.client('s3',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        s3_list = aws_client.list_buckets()
        #print (s3_list)
        for bucket in s3_list['Buckets']:
            #print(bucket)
            location_location_location = aws_client.get_bucket_location(Bucket=bucket['Name'])
            if not 'eu-west-' in location_location_location['LocationConstraint']:
                self.msg = self.msg + ("\nThe bucket " + bucket['Name'] + " is in the zone " + location_location_location['LocationConstraint'])

    def ec2_zone_check(self,user_id,user_pass):
        aws_client = boto3.client('ec2',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        availability_zones = aws_client.describe_availability_zones()
        for zone in availability_zones['AvailabilityZones']:
            if not 'eu-west-' in zone['RegionName']:
                rt = aws_client.describe_route_tables()
                #print(rt)
                for routs in rt['RouteTables']:
                    if routs['Tags']:
                        self.msg = self.msg + ("\nThis ec2 is in the wrong zone " + str(routs['Tags']))



if __name__ == '__main__':
    error_colector = report_upload()
    for user in os.environ:
        if user.startswith('AKI'):
            error_colector.ec2_zone_check(user, os.environ[user])
            error_colector.location_s3_object_lookup(user, os.environ[user])
            error_colector.list_of_domins(user, os.environ[user])
    error_colector.msg = "Hi Team, \n this is the ouput of the report from tonghit \n" + error_colector.msg +" \n This is the output from the Nghitly report \nRegards"
    import smtplib
    msg = """From: """ + os.environ['SUPPORT_EMAIL'] + "\nSubject: Report\n" + error_colector.msg
    s = smtplib.SMTP(os.environ['SMTP_HOST'])
    s.starttls()
    s.set_debuglevel(1)
    s.login(os.environ['SMTP_USERNAME'], os.environ['SMTP_PASSWORD'])
    s.sendmail(os.environ['SUPPORT_EMAIL'], os.environ['SUPPORT_EMAIL'], msg)
