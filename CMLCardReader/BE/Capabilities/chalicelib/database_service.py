import boto3
from collections import defaultdict
from uuid import uuid4 as uuid
from datetime import datetime
import json
class DatabaseService:
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.table_name = 'business-cards'
    
    #get all files from dynamodb
    def get_files(self):
        try:
            response = self.client.scan(TableName=self.table_name)
            if (response is None):
                return None
            return response['Items']
        except self.client.exceptions.ResourceNotFoundException as err:
            print(err)

    #Get file from dynamodb
    def get_file(self, file_id):
        try:
            response = self.client.get_item(
                TableName=self.table_name,
                Key={
                    'partition_id':{
                        'S': '0'
                    },
                    'id': {
                        'S': file_id
                    }
                }
            )
            if (response is None):
                return None
            return response['Item']
        except self.client.exceptions.ResourceNotFoundException as err:
            print(err)
            return None
    def delete_record(self, file_id):
        try:
            response = self.client.delete_item(
                TableName=self.table_name,
                Key={
                    'partition_id':{
                        'S': '0'
                    },
                    'id': {
                        'S': file_id
                    }
                }
            )
            return response
        except BaseException as err:
            print(err)
    #Create business card record
    def create_record(self, file_name, s3_url, entities):
        try:
            id = str(uuid())
            response = self.client.put_item(
                TableName=self.table_name,
                Item={
                    'partition_id':{
                        'S': '0'
                    },
                    'id': {
                        'S': id
                    },
                    'file_name': {
                        'S': file_name if file_name is not None else "test file name"
                    },
                    's3_url': {
                        'S': s3_url if s3_url is not None else "test s3 url"
                    },
                    'entities':{
                        'S': json.dumps(entities)
                    },
                    'created_at': {
                        'S': str(datetime.now())
                    },
                    'updated_at':{
                        'S': str(datetime.now())
                    }
                }
            )
            return {
                "response": response,
                "id": id
            }
        except BaseException as err:
            print(err)
    
    #Update business card record
    def update_file(self, file_id, params):
        if (type(params) is not dict):
            return None
        try:
            response = self.client.update_item(
                TableName=self.table_name,
                Key={
                    'partition_id':{
                        'S': '0'
                    },
                    'id': {
                        'S': file_id
                    }
                },
                UpdateExpression="SET updated_at = :updated_at, entities = :entities",
                ExpressionAttributeValues={
                    ':updated_at': {
                        'S': str(datetime.now())
                    },
                    ':entities': {
                        'S': json.dumps(params)
                    }
                }
            )
            return response
        except self.client.exceptions.ResourceNotFoundException as err:
            print(err)



        
