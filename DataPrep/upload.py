import os
import tqdm
import json
import glob
import requests

from dotenv import load_dotenv
load_dotenv()

def load_data(file_path):
    data = json.load(open(file_path))
    
    converted_data = {
        'name': data['tool_definition']['function']['name'],
        'tool_definition': data['tool_definition'],
        'tool_function': data['tool_function'],
        'instruction': data['instruction']
    }
    
    # return json.dumps(converted_data)
    return converted_data


def upload(file_path):
    
    with open(file_path, 'rb') as f:
        
        data = load_data(file_path)
        
        # Please double check if the S3 target path is correct
        requests.post(
            os.getenv('UPLOAD_ENDPOINT'), 
            headers={'x-api-key': os.getenv('AWS_GATEWAY_API_KEY')},
            json=data
        )
        

if __name__ == '__main__':
    # for file in tqdm.tqdm(glob.glob('sample_output/wikimedia_org_get_metrics_editors_top_by_edits.json')):
    for file in tqdm.tqdm(glob.glob('have_uploaded/*.json')):
        upload(file)
    