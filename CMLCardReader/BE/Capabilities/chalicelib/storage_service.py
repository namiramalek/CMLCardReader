import boto3
from datetime import datetime

class StorageService:
    def __init__(self, storage_location):
        self.client = boto3.client('s3')
        self.bucket_name = storage_location

    def get_storage_location(self):
        return self.bucket_name

    def list_files(self):
        
      try:
        response = self.client.list_objects_v2(Bucket = self.bucket_name)

        files = []
        for content in response['Contents']:
            files.append({
          'location': self.bucket_name,
          'file_name': content['Key'],
          'url': "http://" + self.bucket_name + ".s3.amazonaws.com/"
                + content['Key']
            })
        return files
      except self.client.exceptions.AmazonServiceException as err:
        print(err)




    def upload_file(self, file_bytes, file_name):
      dated_file_name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}{'-'}{file_name}"
      try:
        self.client.put_object(Bucket = self.bucket_name,
                  Body = file_bytes,
                  Key = dated_file_name, 
                  ACL = 'public-read')
        return {'fileId': dated_file_name,
          'fileUrl': "http://" + self.bucket_name + ".s3.amazonaws.com/" + dated_file_name,
          'objectUrl': f'https://s3.amazonaws.com/{self.bucket_name}/{dated_file_name}'
          
          }
      except BaseException as err:
        print(err)