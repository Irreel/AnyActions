def process_swagger_yaml(yaml_content):
    """
    Process Swagger YAML content and split it into separate endpoint-specific YAML files.
    
    Args:
        yaml_content (dict): Parsed YAML content in Swagger format
        
    Returns:
        dict: Dictionary of endpoint-specific YAML contents
            Key: '{method}_{path}' (normalized)
            Value: Dictionary containing the endpoint-specific YAML
    """
    endpoint_specs = {}
    
    # Extract shared components
    shared_components = {
        'info': yaml_content.get('info', {}),
        'swagger': yaml_content.get('swagger', '2.0'),
        'basePath': yaml_content.get('basePath', ''),
        'schemes': yaml_content.get('schemes', []),
        'consumes': yaml_content.get('consumes', []),
        'produces': yaml_content.get('produces', []),
        'definitions': yaml_content.get('definitions', {}),
        'securityDefinitions': yaml_content.get('securityDefinitions', {})
    }
    
    if 'paths' not in yaml_content:
        return endpoint_specs

    # Iterate through each path
    for path, path_data in yaml_content['paths'].items():
        # Iterate through each HTTP method for the path
        for method, method_data in path_data.items():
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                continue
                
            # Create normalized key for the endpoint
            normalized_path = path.replace('/', '_').strip('_')
            endpoint_key = f"{method.lower()}_{normalized_path}"
            
            # Create endpoint-specific YAML
            endpoint_spec = shared_components.copy()
            
            # Add paths section with only this endpoint
            endpoint_spec['paths'] = {
                path: {
                    method: method_data
                }
            }
            
            # If the endpoint has parameters at path level, include them
            if 'parameters' in path_data:
                endpoint_spec['paths'][path]['parameters'] = path_data['parameters']
            
            # Add only required definitions
            required_definitions = extract_required_definitions(
                method_data, 
                yaml_content.get('definitions', {})
            )
            if required_definitions:
                endpoint_spec['definitions'] = required_definitions
            
            endpoint_specs[endpoint_key] = endpoint_spec
            
    return endpoint_specs

def extract_required_definitions(method_data, all_definitions):
    """
    Extract only the definitions required by this endpoint.
    
    Args:
        method_data (dict): The endpoint method data
        all_definitions (dict): All definitions from the original Swagger
        
    Returns:
        dict: Required definitions for this endpoint
    """
    required_definitions = {}
    definitions_to_check = set()
    
    # Check request body schema
    if 'parameters' in method_data:
        for param in method_data['parameters']:
            if param.get('in') == 'body' and 'schema' in param:
                add_schema_definitions(param['schema'], definitions_to_check)
    
    # Check response schemas
    if 'responses' in method_data:
        for response in method_data['responses'].values():
            if 'schema' in response:
                add_schema_definitions(response['schema'], definitions_to_check)
    
    # Add all required definitions
    for def_name in definitions_to_check:
        if def_name in all_definitions:
            required_definitions[def_name] = all_definitions[def_name]
    
    return required_definitions

def add_schema_definitions(schema, definitions_set):
    """
    Recursively find all referenced definitions in a schema.
    
    Args:
        schema (dict): The schema to check
        definitions_set (set): Set to collect definition names
    """
    if isinstance(schema, dict):
        if '$ref' in schema:
            def_name = schema['$ref'].split('/')[-1]
            definitions_set.add(def_name)
        for value in schema.values():
            add_schema_definitions(value, definitions_set)
    elif isinstance(schema, list):
        for item in schema:
            add_schema_definitions(item, definitions_set)