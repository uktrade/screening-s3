import boto3
import os


class screening:
    def __init__(self,aws_use_id,aws_use_pass):
        self.messege = []
        self.aws_client = boto3.client('s3',aws_access_key_id=aws_use_id,aws_secret_access_key=aws_use_pass)
        for buckets_name in self.list_bucket_from_aws():
            self.sceen_bucket(buckets_name)
        #ßprint(self.messege)

    def __iter__(self):
        return self

    def list_bucket_from_aws(self):
        list_buckets=[]
        for bucket in self.aws_client.list_buckets()['Buckets']:
            self.check_bucket(bucket)
            list_buckets.append(bucket['Name'])
        return(list_buckets)


    def check_bucket(self,bucket):
        #print (bucket['Name'])
        try:
         #   print ('The bucket name ' + str(bucket['Name']) + " is trying to get policy ")
            bucket_policy = self.aws_client.get_bucket_policy(Bucket=bucket['Name'])
          #  print(bucket_policy)

        except:
  #          print ('The bucket name ' + str(bucket['Name']) + " have no policy in place ")
            msg = 'The bucket name ' + str(bucket['Name']) + " have no policy in place "
            self.messege.append(msg)
        #check the value of bucket_policy and if we have an issue appand it to self.messege.
        acl = self.aws_client.get_bucket_acl(Bucket=bucket['Name'])
        # run if acl .... self.messege.append('issue whith acl ')

    def check_objet(self, object,buckets_name):
        try:
            object_info = self.aws_client.get_object_acl(Bucket=buckets_name, Key=object)
            print(object)
           # print(object_info['Grants'][0]['Permission'])
            print(set([i['Permission'] for i in object_info['Grants']]))
           # print("\n")
           # print("\n")
           # print("\n")
        except:
            self.messege.append(" this f file have no policy .... file name: " + object)
           # print(" this f file have no policy .... file name: " + object)

    def sceen_bucket(self,buckets_name):
        file_list = self.aws_client.list_objects(Bucket=buckets_name)
        for object in file_list['Contents']:
            self.check_objet(object['Key'],buckets_name)





joe = screening(os.environ['aws_bill_to_gicko_id'],os.environ['aws_bill_to_gicko_pass'])
