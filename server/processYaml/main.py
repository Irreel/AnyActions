import os
import yaml

import processSwagger
import processOpenAPI

def load_openapi_files():
    """
    Load all OpenAPI YAML files from APIdb/openapi directory
    
    Returns:
        dict: Dictionary mapping file paths to parsed YAML content
    """
    openapi_files = {}
    openapi_dir = "APIdb/openapi"
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(openapi_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yaml_content = yaml.safe_load(f)

                        if file == 'openapi.yaml':
                            endpoints = processOpenAPI.process_openapi_yaml(yaml_content)
                            openapi_files[file_path] = endpoints
                            
                        elif file == 'swagger.json':
                            # endpoints = processSwagger.process_swagger_json(yaml_content)
                            # openapi_files[file_path] = endpoints
                            print("Skip swagger.json temporarily")
                            
                        else:
                            raise Exception(f"Unknown file format: {file}")
                        
                        # openapi_files[file_path] = yaml_content
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    continue
            elif file.endswith('.json'):
                print(f"Skip {file} temporarily")
                continue
                    
    return openapi_files

if __name__ == "__main__":
    code = generate_functions('api_spec.yaml')
    with open('api_functions.py', 'w') as f:
        f.write(code)


if __name__ == "__main__":
    load_openapi_files()