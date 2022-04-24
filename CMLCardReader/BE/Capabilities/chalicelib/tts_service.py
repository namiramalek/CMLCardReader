import boto3
from datetime import datetime

class TTSService:
    def __init__(self, storage_service):
        self.client = boto3.client('polly')
        self.storage_service = storage_service

    def get_storage_location(self):
        return self.bucket_name

    def create_audio( self, text, file_name):
        response = self.client.synthesize_speech(
                OutputFormat="mp3",
                Text=text,
                VoiceId="Joanna"
            )
        file_name = f"{file_name}.mp3"
        upload = self.storage_service.upload_file(response['AudioStream'].read(), file_name)
        return upload