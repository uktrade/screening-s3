import json
import requests
import os
import calendar
import operator
from datetime import datetime
import boto3
from math import trunc
import ssl
import pickle
import socket
import threading
from flask import Flask, Response, request, session,render_template
import socket
import time


class aws_index:
    def __init__(self):
        self.msg = ''
        self.today = datetime.now()
        self.index = {}
        self.index_file_content = {}
        self.return_index = {}
        #self.update_from_aws()
        self.update_in_subpros_aws()
        self.update_from_file()

    def update_from_file(self):
        try:
            file_index = open('data/index.json', 'rb')
            self.index_file_content = pickle.loads(file_index.read())
            print ('test_fild --- ')
            print ('test_fild --- ')
            print ('test_fild --- ')
            print (self.index_file_content)
            print ('test_fild --- ')
            print ('test_fild --- ')
            print ('test_fild --- ')
            file_index.close()
        except:
            pass

    def clean_index(self):
        self.index['s3'] = []
        self.index['ec2'] = []
        self.index['cloudfront'] = []
        self.index['route53'] = []
        self.index['acm'] = []
        self.account = ''

    def update_from_aws(self):
        self.clean_index()
        for user in os.environ:
            if user.startswith('AKI'):
                account_id  = boto3.client('sts',aws_access_key_id=user, aws_secret_access_key=os.environ[user])
                self.account = account_id.get_caller_identity().get('Account')
                self.ec2_zone_check(user, os.environ[user])
                self.location_s3_object_lookup(user, os.environ[user])
                self.list_of_domins(user, os.environ[user])
                self.route53_scean(user, os.environ[user])
                self.acm_scean(user, os.environ[user])
        self.return_index = self.index
        index_file = open('data/index.json','wb')
        pickle.dump(self.index_file_content, index_file)
        index_file.close()
        return(True)

    def update_in_subpros_aws(self):
        background_aws_lookup = threading.Thread(target=self.update_from_aws)
        background_aws_lookup.start()

    def list_of_domins(self,user_id, user_pass):
        aws_client = boto3.client('cloudfront',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        ld = aws_client.list_distributions()
        ld['account_need_to_use'] = self.account
        try:
            for item in ld['DistributionList']['Items']:
                for ititems in item['Aliases']['Items']:
                    if not ititems in self.index_file_content:
                        self.index_file_content[ititems] = []
                    self.index_file_content[ititems].append(ld)
        except:
            pass
        self.index['cloudfront'].append(ld)

    def route53_scean(self,user_id,user_pass):
        aws_client = boto3.client('route53',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        r53s = aws_client.list_hosted_zones()
        for zone in r53s['HostedZones']:
            try:
                if not zone['Name'] in self.index_file_content:
                    self.index_file_content[zone['Name']] = []
                self.index_file_content[zone['Name']].append(zone)
            except:
                pass
        self.index['route53'].append(r53s)


    def acm_scean(self,user_id,user_pass):
        aws_client = boto3.client('acm',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        acm = aws_client.list_certificates()
        #print(acm)
        for domanin in acm['CertificateSummaryList']:
            if not domanin['DomainName'] in self.index_file_content:
                self.index_file_content[domanin['DomainName']] = []
            self.index_file_content[domanin['DomainName']].append(domanin)
            print(domanin)
        self.index['acm'].append(acm)


    def location_s3_object_lookup(self,user_id,user_pass):
        aws_client = boto3.client('s3',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        s3_list = aws_client.list_buckets()
        return_index = {}
        for bucket in s3_list['Buckets']:
            return_index[bucket['Name'] + '_bucket'] = bucket
            return_index[bucket['Name']] =  aws_client.list_objects(Bucket=bucket['Name'])
            if not bucket['Name'] in self.index_file_content:
                self.index_file_content[bucket['Name']] = []
            self.index_file_content[bucket['Name']].append(return_index)
        self.index['s3'].append(return_index)


    def ec2_zone_check(self,user_id,user_pass):
        aws_client = boto3.client('ec2',aws_access_key_id=user_id, aws_secret_access_key=user_pass)
        self.index['ec2'].append(aws_client.describe_instances())


#if __name__ == '__main__':
    #jo.update_in_subpros_aws()
    #print(jo.return_index)



app = Flask(__name__)
app.config['DEBUG'] = True




@app.route("/index")
def index_full_json():
    print("start index call ")
    global jo
    return render_template('index.html',INDEX=jo.index_file_content)

@app.route("/index2")
def index2_full_json():
    global jo
    return render_template('index2.html',INDEX=jo.return_index)


jo = {}

print("starting flask ... 1")
jo = aws_index()
print("starting flask ... 2")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))

  #  treed = biils_of_aws
#    tr_aws = threading.Thread(target=biils_of_aws)
#    tr_aws.start()
 #   tr = threading.Thread(target=set_return_hash)
 #   tr.start()
  # this part is not used as this app is stateless and will do nothing bat
