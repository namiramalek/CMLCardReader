import boto3


class TextractService:
    def __init__(self, storage_service):
        self.client = boto3.client('textract')
        self.bucket_name = storage_service.get_storage_location()

    def detect_text(self, file_name):
        try:
            response = self.client.detect_document_text(
                Document = {
                    'S3Object': {
                        'Bucket': self.bucket_name,
                        'Name': file_name
                    }
                }
            )
            lines = []
            response_block = response['Blocks']
            for detection in response_block:
                if detection['BlockType'] == 'LINE':
                    lines.append({
                        'text': detection['Text'],
                        'confidence': detection['Confidence']
                    })

            return lines
        except BaseException as err:
            print(err)
            return None
        