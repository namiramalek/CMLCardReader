import boto3
from collections import defaultdict



class ExtractionService:
    def __init__(self):
        self.comprehend = boto3.client('comprehend')
        self.comprehend_med = boto3.client('comprehendmedical')


    def extract_contact_info_from_file(self, file_name):
        try:
            response = self.comprehend.detect_entities(
                
                Document = {
                    'S3Object': {
                        'Bucket': 'card-data-bucket',
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

    def extract_contact_info(self, contact_string):
        card_information = defaultdict(list)
        
        try:
            # extract info with comprehend
            response_comprehend = self.comprehend.detect_entities(Text = contact_string,LanguageCode = 'en')
            response_entities_comprehend = response_comprehend['Entities']

            for entity in response_entities_comprehend:
                if entity['Type'] == 'PERSON':
                    card_information['name'].append(entity['Text'])
                if entity['Type'] == 'ORGANIZATION':
                    card_information['organization'].append(entity['Text'])
        except self.comprehend.exceptions.UnsupportedLanguageException as err:
            print("err")
        
        try:
           # extract info with comprehend medical
            response_medicalcomprehend = self.comprehend_med.detect_phi(
                Text = contact_string
                )

            response_entities_medicalcomprehend = response_medicalcomprehend['Entities']
            for entity in response_entities_medicalcomprehend:
                if entity['Type'] == 'EMAIL':
                    card_information['email'].append(entity['Text'])
                if entity['Type'] == 'PHONE_OR_FAX':
                    card_information['phone'].append(entity['Text'])
                if entity['Type'] == 'PROFESSION':
                    card_information['title'].append(entity['Text'])
                if entity['Type'] == 'ADDRESS':
                    card_information['address'].append(entity['Text'])
        except self.comprehend_med.exceptions.TextSizeLimitExceededException as err:
            print(err)

        '''# additional processing for address
        address_string = ' '.join(contact_info['address'])
        address_parts = usaddress.parse(address_string)

        for part in address_parts:
            if part[1] == 'PlaceName':
                card_information['city'].append(part[0])
            elif part[1] == 'StateName':
                card_information['state'].append(part[0])
            elif part[1] == 'ZipCode':
                card_information['zip'].append(part[0])'''

        return dict(card_information)
