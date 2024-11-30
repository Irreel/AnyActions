def process_swagger_yaml(yaml_content):
    """
    Process Swagger YAML content and extract API endpoints information.
    
    Args:
        yaml_content (dict): Parsed YAML content in Swagger format
        
    Returns:
        list: List of dictionaries containing endpoint information
            Each dictionary contains:
            - name: NOT IMPLEMENTED
            - method: HTTP method (GET, POST, etc.)
            - path: API endpoint path
    """
    endpoints = []
    
    # Check if paths section exists
    if 'paths' not in yaml_content:
        return endpoints
        
    # Get base path if it exists
    base_path = yaml_content.get('basePath', '')
    
    # Iterate through each path
    for path, path_data in yaml_content['paths'].items():
        # Iterate through each HTTP method for the path
        for method, method_data in path_data.items():
            # Skip if the key is 'parameters' or other non-HTTP method keys
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                continue
                
            # Combine base path with endpoint path
            full_path = base_path + path if base_path else path
            
            endpoint_info = {
                'method': method.upper(),
                'path': full_path,
                # 'summary': method_data.get('summary', '')
            }
            endpoints.append(endpoint_info)
            
    return endpoints


if __name__ == "__main__":
    import yaml
    from pathlib import Path

    # Get the path to the APIdb directory relative to this file
    current_dir = Path(__file__).parent
    api_db_dir = current_dir.parent.parent / 'APIdb' / 'sample'
        
    yaml_path = api_db_dir / 'wikimedia.org' / '1.0.0' / 'swagger.yaml'
    
    with open(yaml_path) as f:
        yaml_content = yaml.safe_load(f)
        
    print(process_swagger_yaml(yaml_content))