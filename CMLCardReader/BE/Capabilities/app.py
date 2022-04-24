from chalice import Chalice
from chalicelib import database_service, extraction_service, storage_service, textract_service, tts_service
import base64
import json
import random
from functools import reduce
app = Chalice(app_name='Capabilities')
app.debug = True

storage_location = 'S3Bucket'
storage_service = storage_service.StorageService(storage_location)
textract_service = textract_service.TextractService(storage_service)
extraction_service = extraction_service.ExtractionService()
database_service = database_service.DatabaseService()
tts_service = tts_service.TTSService(storage_service)

#Get all business cards 8===D
@app.route('/', methods=['GET'], cors=True)
def index():
    files = database_service.get_files() 
    for file in files:
        file['entities']["S"] = json.loads(file['entities']["S"])
    return files


# Get business card by id 8===D
@app.route('/business-card/{file_id}', methods=['GET'], cors=True)
def get_file(file_id):
    file = database_service.get_file(file_id)
    if (file is None): return None
    file['entities']["S"] = json.loads(file['entities']["S"])
    return file

# Update business card 8===D
@app.route('/business-card/{file_id}', methods=['PUT'], cors=True)
def update_business_card(file_id):
    request_data = json.loads(app.current_request.raw_body)
    params = request_data['params']
    if (params is None): return None
    file = database_service.update_file(file_id, params)
    return file


@app.route('/business-card/{file_id}', methods=["DELETE"], cors=True)
def delete_business_card(file_id):
    print(file_id)
    database_service.delete_record(file_id)
    return None

#Upload new business card 8===D
@app.route('/business-card', methods=['POST'], cors=True)
def upload_business_card():
    request_data = json.loads(app.current_request.raw_body)
    img = request_data['img']
    file_name = request_data['fileName']
    if (img is None): return None

    
    img = base64.b64decode(img)
    #save image to S3
    s3_data = storage_service.upload_file(img, file_name)
    #read elements
    elements = textract_service.detect_text(s3_data["fileId"])

    text_only = map(lambda x: x['text'], elements)
    text_only = reduce(lambda x, y: x + ' ' + y, text_only)
    #extract contact info
    contact_info = extraction_service.extract_contact_info(str(text_only))
    #save to dynamodb
    db_record = database_service.create_record(s3_data["fileId"], s3_data["fileUrl"], contact_info)    
    return db_record



@app.route('/business-card/{file_id}/tts', methods=['POST'], cors=True)
def text_to_speech(file_id):
    file = database_service.get_file(file_id)
    if (file is None): return None
    file['entities']["S"] = json.loads(file['entities']["S"])
    #convert dict to key value pairs 
    entities_dict = file["entities"]["S"]
    #convert dict values from list to string
    entities_dict = {k: reduce(lambda x, y: x + ' ' + y, v) for k, v in entities_dict.items()}
    #convert dict values from string to list
    entities_dict = {k: v.split() for k, v in entities_dict.items()}
    #convert dict values from list to string
    entities_dict = {k: reduce(lambda x, y: x + ' ' + y, v) for k, v in entities_dict.items()}
    #convert dict to list of tuples
    entities_list = [(k, v) for k, v in entities_dict.items()]
    entities_list = list(map(lambda kv: (kv[0] + ": " + kv[1]), entities_list))
    text_to_read = reduce(lambda x, y: x + '. ' + y, entities_list)

    tts_file = tts_service.create_audio(text_to_read, file_id)
    return tts_file



#Extract text from business card image
@app.route('/images/{image_id}/extract_info', cors = True)
def extract_info(image_id):
    files = storage_service.list_files()
    images = [file for file in files if file['file_name'].endswith(".jpg")]
    image_file = random.choice(images)

    text = textract_service.detect_text(image_id)
    MIN_CONFIDENCE = 70.0
   
    contact_lines = []
    
    for line in text:
        if float(line['confidence']) >= MIN_CONFIDENCE:
            contact_lines.append(line['text'])
    information = ' '.join(contact_lines)
   
    card_info = extraction_service.extract_contact_info(information)
    return card_info
 
