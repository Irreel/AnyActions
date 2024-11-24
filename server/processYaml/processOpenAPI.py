import yaml
from jinja2 import Template
import logging

def process_openapi_yaml(yaml_content):
    """
    Process OpenAPI YAML content and extract API endpoints information.
    
    Args:
        yaml_content (dict): Parsed YAML content in OpenAPI format
        
    Returns:
        list: List of dictionaries containing endpoint information
            Each dictionary contains:
            - name: API endpoint name (operationId) The naming rule may be inconsistent.
            - method: HTTP method (GET, POST, etc.)
            - path: API endpoint path
    """
    endpoints = []
    
    # Check if paths section exists
    if 'paths' not in yaml_content:
        return endpoints
        
    # Iterate through each path
    for path, path_data in yaml_content['paths'].items():
        
        # Iterate through each HTTP method for the path
        for method, method_data in path_data.items():
            operation_id = method_data.get('operationId')
            
            endpoint_info = {
                'name': operation_id,
                'method': method.upper(),
                'path': path
            }
            endpoints.append(endpoint_info)
            
    return endpoints


def generate_client_functions_openapi(spec):

    base_url = spec.get('servers', [{'url': '/'}])[0]['url']
    paths = spec.get('paths', {})

    function_template = Template("""
{% for path, methods in paths.items() %}
{% for method, details in methods.items() %}
def {{ details.get('operationId', method + '_' + path.replace('/', '_').strip('_')) }}({% if details.get('parameters') %}{% for param in details.parameters %}{% if param.in == 'query' or param.in == 'path' %}{{ param.name }}{% if not loop.last %}, {% endif %}{% endif %}{% endfor %}{% endif %}{% if details.get('requestBody') %}{% if details.get('parameters') %}, {% endif %}data{% endif %}):
    \"\"\"{{ details.get('summary', '') }}\"\"\"
    import requests
    url = f"{{ base_url }}{{ path }}"
    {% if details.get('parameters') %}
    {% for param in details.parameters %}
    {% if param.in == 'path' %}
    url = url.format({{ param.name }}={{ param.name }})
    {% endif %}
    {% endfor %}
    {% endif %}
    params = {
        {% if details.get('parameters') %}
        {% for param in details.parameters %}
        {% if param.in == 'query' %}
        "{{ param.name }}": {{ param.name }},
        {% endif %}
        {% endfor %}
        {% endif %}
    }
    {% if details.get('requestBody') %}
    data = data
    {% else %}
    data = None
    {% endif %}
    response = requests.{{ method }}(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
{% endfor %}
{% endfor %}
""")

    functions_code = function_template.render(paths=paths, base_url=base_url)
    return functions_code


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        filename='gen.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        with open('../APIdb/sample/brex.io/2021.12/openapi.yaml', 'r') as f:
            spec = yaml.safe_load(f)
            
        code = generate_client_functions_openapi(spec)
        
        with open('client.py', 'w') as f:
            f.write(code)
        
        logging.info('Successfully generated base functions and wrote to base.py')
    except Exception as e:
        logging.error(f'Error processing OpenAPI YAML: {str(e)}')
        
        