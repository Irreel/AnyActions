import os
import json
import yaml
import dotenv
from openai import OpenAI
from formats import *
from typing import Callable

from processYaml.processOpenAPI import endpoint_from_openapi_yaml
from processYaml.processSwagger import endpoint_from_swagger_yaml
from prompts import *


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


def genDscpFromYaml(endpoint: dict, source_yaml: dict) -> str:
    """
    Generate the API description from the loadedyaml file

    Args:
        endpoint (dict): the endpoint to generate description for
        source_yaml (dict): the dict get from yaml.safe_load(open(source_yaml_path, 'r'))

    Returns:
        str: the generated API description
        
    endpoint(dict) is defined at processOpenAPI.py as:
        endpoint_info = {
            'name': operation_id,
            'operationId': operation_id,
            'method': method.upper(),
            'path': path
        }
    """
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = genDscpFromYaml_withNoExec.replace('{source_yaml}', str(source_yaml)).replace('{target_endpoint}', str(endpoint))

    try:
        completion = client.chat.completions.create(
            model="o1-mini-2024-09-12",
            messages=[  
                {"role": "user", "content": prompt + structuredResponse},
                {"role": "assistant", "content": "```json\n{\n"}
            ],
            )
        
        response = completion.choices[0].message.content
        
        # Somehow the pydantic model with dict doesn't work
        # completion = client.beta.chat.completions.parse(
        #     model="gpt-4o",
        #     messages=[  
        #         {"role": "user", "content": prompt + structuredResponse}
        #     ],
        #     response_format=
        # )
        # response = completion.choices[0].message.parsed
        
        print(f"model response: {response}")
        
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
    # Parse the JSON string into a Python dict
    response_dict = json.loads(response)
    
    try:
        # Validate against the Pydantic model
        validated_response = rawResponseWithNoExec(**response_dict)
        return True
    
    except Exception as e:
        print(response_dict)
        print(f"Invalid response format: {str(e)}")
        return False


def shortenOpenapiYaml_single(endpoint: dict, yaml_path: str):
    """
    Shorten the yaml file to only include the target endpoint and context
    Only support OpenAPI since it searches by operationId
    
    Args:
        endpoint (dict): Dictionary containing endpoint information including operationId
        yaml_path (str): Path to the OpenAPI YAML file
        
    Returns:
        dict: Shortened YAML dictionary containing only relevant endpoint info and API provider details
        
    OpenAPI Specification: https://swagger.io/specification/#:~:text=An%20OpenAPI%20document%20that%20conforms,in%20JSON%20or%20YAML%20format.
    """
    try:
        with open(yaml_path, 'r') as f:
            full_yaml = yaml.safe_load(f)
            
        # Create new yaml with only necessary parts
        shortened_yaml = {
            # Keep API provider info
            'openapi': full_yaml.get('openapi'),
            'info': full_yaml.get('info'),
            'servers': full_yaml.get('servers', '/'),
            'security': full_yaml.get('security', []),
            'tags': full_yaml.get('tags', []),
            'externalDocs': full_yaml.get('externalDocs', {}),
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

def shortenOpenapiYaml(yaml_path: str, endpoint_extractor: Callable = endpoint_from_openapi_yaml):
    """
    An iterator that shortens the full yaml file to only include one endpoint and context at a time
    Only support OpenAPI since it searches by operationId
    
    Args:
        yaml_path (str): Path to the full OpenAPI YAML file
        endpoint_extractor (Callable): The function to extract the endpoints from the yaml file. By default, it supports openapi yaml
        
    Returns:
        tuple: (endpoint, shortened_yaml)
        
    OpenAPI Specification: https://swagger.io/specification/#:~:text=An%20OpenAPI%20document%20that%20conforms,in%20JSON%20or%20YAML%20format.
    """
    try:
        with open(yaml_path, 'r') as f:
            full_yaml = yaml.safe_load(f)
            
        # Create new yaml with only necessary parts
        shortened_yaml_template = {
            # Keep API provider info
            'openapi': full_yaml.get('openapi'),
            'info': full_yaml.get('info'),
            'servers': full_yaml.get('servers', '/'),
            'security': full_yaml.get('security', []),
            'tags': full_yaml.get('tags', []),
            'externalDocs': full_yaml.get('externalDocs', {}),
            'paths': {}
        }
        
        # Get all the paths
        endpoints = endpoint_extractor(full_yaml)
        
        for endpoint in endpoints:
            try:
                endpoint_path = endpoint['path']
                item = full_yaml['paths'][endpoint_path]
                shortened_yaml = shortened_yaml_template
                shortened_yaml['paths'][endpoint_path] = item
                
                yield endpoint, shortened_yaml
            except Exception as e:
                print(f"Error shortening OpenAPI YAML for {str(endpoint)[:10]}: {e}")
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    
    # Read the local yaml file
    DATA_DIR = '../APIdb/sample_todo'
    OUTPUT_DIR = './sample_output'
    for service_provider in os.listdir(DATA_DIR):
        for root, dirs, files in os.walk(DATA_DIR + '/' + service_provider):
            for file in files:
                if file.endswith('.yaml'):
                    yaml_path = os.path.join(root, file)
                    print(f"Processing {yaml_path}")
                    
                    # Choose a endpoint extractor based on the file name. Noticed we only consider files end with .yaml
                    if file.startswith('openapi'):
                        endpoint_extractor = endpoint_from_openapi_yaml
                    elif file.startswith('swagger'):
                        endpoint_extractor = endpoint_from_swagger_yaml
                        raise NotImplementedError   
                    else:
                        print(f"Unsupported type for now {str(file)}")
                        continue
                    
                    for endpoint, single_yaml in shortenOpenapiYaml(yaml_path, endpoint_extractor):
                        max_retries = 3
                        retry_count = 0
                        while retry_count < max_retries:
                            r = genDscpFromYaml(endpoint, single_yaml)
                            try:
                                if r.startswith('```json') and r.endswith('```'):
                                    r = r[7:-3].strip('\n')
                                    
                                # Check the format
                                try:
                                    endpoint_name = json.loads(r).get('tool_definition', {}).get('function', {}).get('name', 'unnamed')
                                except Exception as e:
                                    endpoint_name = endpoint.get('name', 'unnamed')
                                    print(f"Error parsing response for {endpoint_name}: {e}")
                                    print(r)
                                    raise Exception
                                
                                assert responseFormatCheck(r), f"Invalid response format for {endpoint_name}"
                                
                                output_path = os.path.join(OUTPUT_DIR, f"{endpoint_name}.json")
                                with open(output_path, 'w') as f:
                                    f.write(r)
                                    
                                break
                                         
                            except Exception as e:
                                retry_count += 1
                                print(f"Error parsing response for {endpoint.get('name', 'unnamed')} (Attempt {retry_count}/{max_retries}): {e}")
                                print(r)
                                if retry_count == max_retries:
                                    print(f"Failed to parse response after {max_retries} attempts")
                                    print(endpoint)
                        
                    
                    
