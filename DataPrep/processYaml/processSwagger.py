def endpoint_from_swagger_yaml(yaml_content):
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
        raise ValueError("No paths found in the YAML content")
        
    host = yaml_content.get('host', '')
    
    # Get base path if it exists
    base_path = yaml_content.get('basePath', '')
    if len(base_path) == 0:
        base_path = yaml_content.get('servers', [{}])[0].get('url', '')
    
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