import boto3



class screening:
    def __init__(self,aws_use_id,aws_use_pass):
        self.messege = False
        self.object_list = []
        self.aws_client = boto3.client('s3',aws_access_key_id=aws_use_id,aws_secret_access_key=aws_use_pass)
        self.list_bucket_from_aws()
        for backts_name in self.list_bucket_from_aws():
            self.sceen_bucket(buckets_name)


    def list_bucket_from_aws(self):
        list_buckets=[]
        for backet in self.aws_client.list_buckets()['Buckets']:
            self.check_backet(backet)
            list_buckets.append(backet['Name'])
        return(list_buckets)


    def check_backet(self,backet):
        pass


    def check_objet(self,object):
        pass

    def sceen_bucket(self,buckets_name):
        file_list = self.aws_client.list_objects(Bucket=backets_name)
        for object in file_list:
            self.check_objet(object['Key'])
