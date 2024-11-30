"""
    Mocking the AAPI server response for use cases
"""

import requests
from ..db_tmp import db_index


def get_tool_calling_function(tool_name):
    
    if tool_name == "GOOGLE_SEARCH":
        response = mock_request()
        
        if response['gen_flg'] == 0:
            return response['instruction'], json.loads(response['tool_definition']), response['tool_calling_function'], response['exec_sh']
        
        elif response['gen_flg'] == 1:
            # TODO: this tool calling function is generated
            raise NotImplementedError
    
    else:
        raise NotImplementedError
    
    
def mock_request(tool_name='GOOGLE_SEARCH'):
    """
    Return:
        gen_flg: if it is generated or not
        instruction: API register link and instruction (str)
        tool_definition: tool description (OpenAI tool calling format)
        tool_calling_function: tool_calling_function.py
        exec_sh: optional .sh command
    """
    response = {
        "gen_flg": 0,
        "instruction": "http://serpapi.com",
        "tool_definition": { 
            "name": "google_search",
            "description": "Performs a Google search for the given query",
            "input_schema": {
                "type": "object",
                "properties": {
                "q": {
                    "type": "string",
                        "description": "The search query to be used for the Google search"
                    }
                },
                "required": ["q"]
            }
        },
        "tool_calling_function": str(google_search_tool.__code__),
        "exec_sh": None
    }
    return response


def google_search_tool(query, api_key):
    """_tool_definition_
    [This is the tool definition passing to the LLM]
    { 
        "name": "google_search",
        "description": "Performs a Google search for the given query",
        "input_schema": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "The search query to be used for the Google search"
                }
            },
            "required": ["q"]
        }
    }
    """
    if api_key is None:
        api_key = 'c0845552af56b310e230b600fccee6464c5deb0fe2a474b7a3ee28c6314544f7'
    
    # Configuration for the API
    endpoint = "https://serpapi.com/search"
    input_schema = {
        "q": "Parameter defines the query you want to search."
    }

    # Validate input
    if not query or not isinstance(query, str):
        raise ValueError(f"Invalid query provided. Expected a non-empty string, got: {query}")

    # Prepare request parameters
    params = {
        "q": query,
        "api_key": api_key
    }

    # Make the API request
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to parse response JSON: {e}")

    # Optionally: Validate response against output_schema (not implemented here)
    
    return data


def wikipedia_search_tool():
    pass

def jira_search_dashboard_tool():
    pass
