import os
import yaml
import dotenv
from openai import OpenAI
from constants import *

from processYaml.processOpenAPI import process_openapi_yaml
from prompts import *


"""
This function generates an API description file which includes:
    the tool description passed to LLM
    the function description
    the function parameters description
"""


def genDscpFromYaml(endpoint: dict, source_yaml_path: str):
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
    
    source_yaml = yaml.safe_load(open(source_yaml_path, 'r'))
    prompt = genDscpFromYaml_withNoExec.replace('{source_yaml}', str(source_yaml)).replace('{target_endpoint}', str(endpoint))

    try:
        # completion = client.beta.chat.completions.parse(
        #     # model="o1-mini-2024-09-12",
        #     model="gpt-4o-2024-11-20",
        #     messages=[  
        #         {"role": "user", "content": prompt + structuredResponse}
        #     ],
        #     # response_format=rawResponseWithNoExec,
        #     )
        
        completion = client.chat.completions.create(
            model="o1-mini-2024-09-12",
            # model="gpt-4o-2024-11-20",
            messages=[  
                {"role": "user", "content": prompt + structuredResponse}
            ]
            )
        
        response = completion.choices[0].message.content
        
        return response
        
    except Exception as e:
        print(f"Error generating description for {endpoint['name']}: {e}")


def responseFormatCheck(response: str):
    """
    Validates if the response string follows the required format using the rawResponseWithNoExec model.
    
    Args:
        response (str): The JSON response string to validate
        
    Returns:
        bool: True if the response matches the model
        
    Raises:
        ValueError: If the response format is invalid
    """
    try:
        # Parse the JSON string into a Python dict
        response_dict = json.loads(response)
        
        # Validate against the Pydantic model
        validated_response = rawResponseWithNoExec(**response_dict)
        return True
        
    except Exception as e:
        raise ValueError(f"Invalid response format: {str(e)}")


def shortenYaml(endpoint: dict, yaml_path: str):
    raise NotImplementedError

if __name__ == "__main__":
    # Try generated from the sample yaml set
    DATA_DIR = '/Users/zhao/Documents/Startup/ProjActions/AnyActions/APIdb/sample'
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.yaml'):
                yaml_path = os.path.join(root, file)
                print(f"Processing {yaml_path}")
                yaml_content = yaml.safe_load(open(yaml_path, 'r'))
                endpoints = process_openapi_yaml(yaml_content)
                for endpoint in endpoints:
                    r = genDscpFromYaml(endpoint, yaml_path)
                    
                    with open('output.log', 'a') as f:
                        f.write(f"\n\n=== Processing endpoint {endpoint.get('name', 'unnamed')} from {yaml_path} ===\n")
                        f.write(r)
                        f.write("\n")
                    
                    raise ValueError("Stop here")
                
