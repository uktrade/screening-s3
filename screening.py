import boto3
import os


class screening:
    def __init__(self,aws_use_id,aws_use_pass):
        self.messege = []
        self.object_list = []
        self.aws_client = boto3.client('s3',aws_access_key_id=aws_use_id,aws_secret_access_key=aws_use_pass)
        for buckets_name in self.list_bucket_from_aws():
            self.sceen_bucket(buckets_name)

    def __iter__(self):
        return self

    def list_bucket_from_aws(self):
        list_buckets=[]
        for bucket in self.aws_client.list_buckets()['Buckets']:
            self.check_bucket(bucket)
            list_buckets.append(bucket['Name'])
        return(list_buckets)


    def check_bucket(self,bucket):
        print (bucket)
        try:
            bucket_policy = self.aws_client.get_bucket_policy(Bucket=bucket)
        except:
            msg = 'The bucket name ' + bucket + " have no policy in place "
            self.messege.append(msg)
        #check the value of bucket_policy and if we have an issue appand it to self.messege.
        acl = self.aws_client.get_bucket_acl(Bucket=bucket)
        # run if acl .... self.messege.append('issue whith acl ')

    def check_objet(self, object):
        #print(object)
        pass

    def sceen_bucket(self,buckets_name):
        file_list = self.aws_client.list_objects(Bucket=buckets_name)
        for object in file_list['Contents']:
            self.check_objet(object['Key'])





joe = screening(os.environ['aws_bill_to_gicko_id'],os.environ['aws_bill_to_gicko_pass'])
