import os
import json
import yaml
import dotenv
from openai import OpenAI
from formats import *

from processYaml.processOpenAPI import process_openapi_yaml
from processYaml.processSwagger import process_swagger_yaml
import prompts


"""
This function generates an API description file which includes:
    the tool description passed to LLM
    the function description
    the python function
"""


def genDscpFromSearch(api_name: str, api_provider: str):
    """
    Please check genAPIByByob.ipynb for more details
    """
    pass


def genDscpFromYaml(endpoint: dict, source_yaml_path: str):
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
    
    source_yaml = yaml.safe_load(open(source_yaml_path, 'r'))
    prompt = genDscpFromYaml_withNoExec.replace('{source_yaml}', str(source_yaml)).replace('{target_endpoint}', str(endpoint))

    try:
        completion = client.chat.completions.create(
            model="o1-mini-2024-09-12",
            # model="gpt-4o-2024-11-20",
            messages=[  
                {"role": "user", "content": prompt + prompts.structuredResponse}
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
        print(response_dict)
        print(f"Invalid response format: {str(e)}")
        return False


def shortenOpenapiYaml(endpoint: dict, yaml_path: str):
    """
    Shorten the yaml file to only include the target endpoint and context
    Only support OpenAPI since it searches by operationId
    
    Args:
        endpoint (dict): Dictionary containing endpoint information including operationId
        yaml_path (str): Path to the OpenAPI YAML file
        
    Returns:
        dict: Shortened YAML dictionary containing only relevant endpoint info and API provider details
    """
    try:
        with open(yaml_path, 'r') as f:
            full_yaml = yaml.safe_load(f)
            
        # Create new yaml with only necessary parts
        shortened_yaml = {
            # Keep API provider info
            'openapi': full_yaml.get('openapi'),
            'info': full_yaml.get('info'),
            'servers': full_yaml.get('servers'),
            'tags': full_yaml.get('tags'),
            'paths': {}
        }
        
        # Find the path containing our target operationId
        target_path = None
        target_method = None
        
        for path, methods in full_yaml.get('paths', {}).items():
            for method, details in methods.items():
                if details.get('operationId') == endpoint.get('name'):
                    target_path = path
                    target_method = method
                    break
            if target_path:
                break
                
        if target_path:
            shortened_yaml['paths'][target_path] = {target_method: full_yaml['paths'][target_path][target_method]}
                
        return shortened_yaml
        
    except Exception as e:
        print(f"Error shortening OpenAPI YAML for {endpoint['name']}: {e}")

if __name__ == "__main__":
    # Try generated from the sample yaml set
    DATA_DIR = '../APIdb/sample'
    OUTPUT_DIR = './sample_output'
    for service_provider in os.listdir(DATA_DIR):
        for root, dirs, files in os.walk(DATA_DIR + '/' + service_provider):
            for file in files:
                if file.endswith('.yaml'):
                    yaml_path = os.path.join(root, file)
                    print(f"Processing {yaml_path}")
                    yaml_content = yaml.safe_load(open(yaml_path, 'r'))
                    if file.startswith('openapi'):
                        endpoints = process_openapi_yaml(yaml_content)
                    elif file.startswith('swagger'):
                        endpoints = process_swagger_yaml(yaml_content)
                    else:
                        print(f"Unsupported type for now {str(file)}")
                        continue
                    for endpoint in endpoints:
                        r = genDscpFromYaml(endpoint, yaml_path)
                        
                        if r.startswith('```json') and r.endswith('```'):
                            r = r[7:-3].strip('\n')
                        
                        try:
                            endpoint_name = json.loads(r).get('tool_definition', {}).get('function', {}).get('name', 'unnamed')
                        except Exception as e:
                            print(f"Error parsing response for {endpoint.get('name', 'unnamed')}: {e}")
                            print(r)
                            endpoint_name = endpoint.get('name', 'unnamed')
                        
                        if responseFormatCheck(r):
                            print(f"Valid response format for {endpoint_name}")
                        else:
                            print(f"Invalid response format for {endpoint_name}")
                            print(r)
                            raise Exception
                    
                        with open(OUTPUT_DIR + '/' + endpoint_name + '.json', 'a') as f:
                            # f.write(f"\n\n=== Processing endpoint {endpoint.get('name', 'unnamed')} from {yaml_path} ===\n")
                            f.write(r)
                            # f.write("\n")
                    
