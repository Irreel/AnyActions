import json
import inspect
from typing import List
from pathlib import Path
from .base.decorators import *

from .register_api_tmp import *
from .db_tmp import db, db_index, tool_name_to_index # db_tmp is to stimulate the real database


def store_calling_function(model_response, tool_name, path):
    """Save model response to a Python file at the specified path
    
    Args:
        model_response: The response from the model
        path: File path to save the response
    """
        
    try:
        with open(path + f"{tool_name}.py", 'w') as f:
            f.write(str(model_response))
        return True
    
    except Exception as e:
        print(f"Error saving model response: {e}")
        return False


def create_inter_api_key(legal_api_name, api_dir_path, user, api_key_flg=1):
    """_summary_
    inter_api_key: refers to the 3rd party API key (We call it locally for now, might use it for future server to call them)
    
    Args:
        legal_api_name (_type_): A legal api name is formatted as [PROVIDER NAME]_[ACTION NAME] in upperletters
        api_dir_path: [Temporary] Keep the api key in local file
        user: For now, just a placeholder for user information
    Results:
        True, inter_api_key: create the api key successful
        True, '': the api key is optional and user did not provide one
        True, None: this api does not need api
        False, None: the request failed
    """
    try:
        provider_name, action_name = legal_api_name.split("_", maxsplit=1)
    except:
        print("Illegal API name. Please formatted as '[PROVIDER NAME]_[ACTION NAME]' in string")
    
    try:
        
        assert db[provider_name][action_name]["api_key_flg"] != 0 # Optional, removed if it called remote server
        
        match db[provider_name][action_name]: # The action exists
            case _:
                
                # TODO: For now it is just a stub code asking user to enter it manually / pretend it retrieves from a remote server
                if api_key_flg == 2:
                    print(f"\nAPI key is optional for {legal_api_name}. More details: {db[provider_name][action_name]['documentation']}")
                    x = input("Please enter the API key if you want to use it: ")
                    if x:
                        inter_api_key = x
                    else:
                        inter_api_key = ''
                        
                elif legal_api_name == "GOOGLE_SEARCH":
                    inter_api_key = register_api_tmp[legal_api_name]
                    
                with open(api_file_path, 'w') as f:
                    f.write(f"ACTION_{legal_api_name}_KEY = '{inter_api_key}'\n")
                if len(inter_api_key) > 0:
                    print(f"Created a new API key for {legal_api_name} and saved into {api_dir_path}")
                else:
                    print(f"Created an empty API key for {legal_api_name} and saved into {api_dir_path}")
                
                return True, inter_api_key
            
            
            # TODO: Register a API key for developers? [HasBeenDiscussed]
            
            # TODO: There might be some APIs need to install their own libary mandatory. Maybe we can download those library in user local folder automatically?
                # Run terminal command to install their library
                # try:
                #     import subprocess
                #     subprocess.check_call(["pip", "install", "atlassian-python-api"])
                #     print("Successfully installed JIRA library")
                #     inter_api_key = input("Please enter your JIRA API token: ")
                #     return True, inter_api_key
                # except subprocess.CalledProcessError as e:
                #     print(f"Failed to install JIRA library: {e}")
                #     return False, None
                
            
        
    except Exception as e:
        print(e)
        return False, None
  
    
@deprecated
def definition(tool_list: List) -> List[dict]:
        """_summary_
        Args:
            tool_list: a list of tools to define. Each entry can be:
                - A string representing a pre-defined tool name
                - A dictionary containing a custom tool definition
                - A callable function (not yet implemented)

        This method processes the provided tool list and returns a list of tool definitions.
        For predefined tools (strings), it looks up the definition in the db_index.
        For custom tools (dictionaries), it adds them directly to the list.
        For callable functions, it's going to generate the definition based on the code.

        Raises:
            NotImplementedError: _description_

        Returns:
            List[dict]: _description_
        """

        if not isinstance(tool_list, list): tool_list = [tool_list]
        
        tool_definition_list = []
        for entry in tool_list:
            match entry:
                case str():
                    # If it is a tool name
                    legal_api_name = tool_name_to_index.get(entry, None) # tool_name_to_index is a stub code to stimulate the real database
                    if legal_api_name:
                        # RANDOM IDEA: Add a local mapping between tool name and legal api name?
                        provider_name = legal_api_name.split("_")[0]
                        action_name = legal_api_name.split("_", 1)[1]
                        tool_definition_list.append(db[provider_name][action_name]['ai_tool_desc'])
                        
                    else:
                        print(f"{entry} is not found in actions library")
                        tool_definition_list.append(entry)
                case dict():
                    tool_definition_list.append(entry)
                case callable():
                    # TODO
                    function_body = inspect.getsource(entry) 
                    # function_body = entry.__code__.co_code.decode()
                    print("An experimental function: get tool description from its code body (also generated by LLM?)")
                    print(function_body)
                    
                    tool_definition_list.append(function_to_json(entry))
                    
                case _:
                    raise ValueError("Unsupported tool type")
        
        return tool_definition_list
    

def parse_tool_definition(local_env_path, tool_name: str) -> dict:
    """
    Parses the _tool_definition_ from the specified Python file.

    Args:
        local_env_path (Path): The path to the local environment directory.
        tool_name (str): The name of the tool file (e.g., 'tool_calling_test.py').

    Returns:
        dict: The parsed tool definition.
    """
    
    tool_path = Path(local_env_path) / tool_name
    
    try:
        with tool_path.open('r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Tool calling function not found at path: {tool_path}")

    try:
        # Find the start of the _tool_definition_ docstring
        start_marker = '"""_tool_definition_'
        start_index = content.find(start_marker)
        if start_index == -1:
            raise ValueError("Start marker for _tool_definition_ not found.")

        # Find the end of the docstring
        end_marker = '"""'
        end_index = content.find(end_marker, start_index + len(start_marker))
        if end_index == -1:
            raise ValueError("End marker for _tool_definition_ not found.")

        # Extract the JSON part within the docstring
        docstring_content = content[start_index + len(start_marker):end_index].strip()

        # Assuming the JSON starts after the description line
        json_start = docstring_content.find('{')
        json_str = docstring_content[json_start:]

        # Parse the JSON string into a dictionary
        tool_definition = json.loads(json_str)
    except Exception as e:
        print(f"Failed to parse tool definition: {e}\nParse to json directly")
        return function_to_json(content)

    return tool_definition
    

def write_tool_to_local(api_dir_path: str, tool_definition: dict, tool_func: str, exec_sh = None):
    """
    Args:
        api_dir_path (str): Path to write the tool file
        tool_definition (dict): Tool definition in OpenAI format
        tool_func (str): Function code as string
        exec_sh (str, optional): Shell commands to execute. Defaults to None.
    """
    tool_name = tool_definition["name"]
    file_path = Path(api_dir_path) / f"{tool_name}.py"

    try:
        with file_path.open('w', encoding='utf-8') as f:
            # Write the tool definition as a docstring
            f.write('"""_tool_definition_\n')
            f.write(json.dumps(tool_definition, indent=4))
            f.write('\n"""\n\n')

            ## if Claude
            # # Prepare function parameters from input_schema
            # input_schema = tool_definition.get("input_schema", {})
            # properties = input_schema.get("properties", {})
            # required = input_schema.get("required", [])
            
            ## if OpenAI
            # input_schema = tool_definition.get("function", {}).get("parameters", {})
            # properties = input_schema.get("properties", {})
            # required = input_schema.get("required", [])
            # param_list = []
            # for param in properties.items():
            #     param_name = param.key
            #     param_attrs = param.value["type"]
            #     if param_name in required:
            #         param_list.append(f"{param_name}")
            #     else:
            #         default = param_attrs.get("default", "None")
            #         param_list.append(f"{param_name}={default}")
            # params = ", ".join(param_list)
            
            # Write function body with proper indentation
            func_body = tool_func.split('\n')
            for line in func_body:
                f.write('    ' + line + '\n')

        if exec_sh:
            # Execute any shell commands if provided
            subprocess.run(exec_sh, shell=True, check=True)
            
    except Exception as e:
        raise Exception(f"Failed to write tool to {file_path}: {e}")
    

def function_to_json(func) -> dict:
    """
    https://github.com/openai/swarm?tab=readme-ov-file#examples

    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def parse_model_response(model_response):
    """
    Parse different model response
    """
    pass


def check_dependencies(tool_list: List):
    """
    Check if the tool_list has all the dependencies
    """
    # TODO: request to the server?
    
    
    def check_tool_definition(tool_definition: dict):
    """
    Validates the tool_definition dictionary to ensure it follows the required format.

    Expected Format:
    {
        "type": "function",
        "function": {
            "name": "function_name",
            "description": "Function description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Description of param1."
                    },
                    ...
                },
                "required": ["param1", ...],
                "additionalProperties": False
            }
        }
    }

    Args:
        tool_definition (dict): The tool definition to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        ValueError: If any validation check fails.
    """
    import json

    # Define the required top-level keys
    required_top_level = {"type", "function"}
    if not isinstance(tool_definition, dict):
        raise ValueError("Tool definition must be a dictionary.")

    missing_keys = required_top_level - tool_definition.keys()
    if missing_keys:
        raise ValueError(f"Missing top-level keys: {missing_keys}")

    if tool_definition["type"] != "function":
        raise ValueError("The 'type' field must be 'function'.")

    function_details = tool_definition.get("function")
    if not isinstance(function_details, dict):
        raise ValueError("The 'function' field must be a dictionary.")

    # Required keys within 'function'
    required_function_keys = {"name", "description", "parameters"}
    missing_function_keys = required_function_keys - function_details.keys()
    if missing_function_keys:
        raise ValueError(f"Missing keys in 'function': {missing_function_keys}")

    # Validate 'name'
    if not isinstance(function_details["name"], str):
        raise ValueError("The 'name' field must be a string.")

    # Validate 'description'
    if not isinstance(function_details["description"], str):
        raise ValueError("The 'description' field must be a string.")

    # Validate 'parameters'
    parameters = function_details.get("parameters")
    if not isinstance(parameters, dict):
        raise ValueError("The 'parameters' field must be a dictionary.")

    # Check required keys in 'parameters'
    required_parameters_keys = {"type", "properties", "required", "additionalProperties"}
    missing_parameters_keys = required_parameters_keys - parameters.keys()
    if missing_parameters_keys:
        raise ValueError(f"Missing keys in 'parameters': {missing_parameters_keys}")

    if parameters["type"] != "object":
        raise ValueError("The 'type' field in 'parameters' must be 'object'.")

    # Validate 'properties'
    properties = parameters.get("properties")
    if not isinstance(properties, dict):
        raise ValueError("The 'properties' field must be a dictionary.")

    for prop, details in properties.items():
        if not isinstance(details, dict):
            raise ValueError(f"The details of property '{prop}' must be a dictionary.")
        if "type" not in details or "description" not in details:
            raise ValueError(f"Property '{prop}' must have 'type' and 'description' fields.")
        if not isinstance(details["type"], str):
            raise ValueError(f"The 'type' of property '{prop}' must be a string.")
        if not isinstance(details["description"], str):
            raise ValueError(f"The 'description' of property '{prop}' must be a string.")

    # Validate 'required'
    required_fields = parameters.get("required")
    if not isinstance(required_fields, list):
        raise ValueError("The 'required' field must be a list.")
    for field in required_fields:
        if field not in properties:
            raise ValueError(f"Required field '{field}' is not defined in 'properties'.")

    # Validate 'additionalProperties'
    if not isinstance(parameters["additionalProperties"], bool):
        raise ValueError("The 'additionalProperties' field must be a boolean.")

    # If all checks pass
    return True


def check_tool_definition(tool_definition: dict):
    """
    Validates the tool_definition dictionary to ensure it follows the required format.

    Expected Format:
    {
        "type": "function",
        "function": {
            "name": "function_name",
            "description": "Function description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Description of param1."
                    },
                    ...
                },
                "required": ["param1", ...],
                "additionalProperties": False
            }
        }
    }

    Args:
        tool_definition (dict): The tool definition to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        ValueError: If any validation check fails.
    """
    import json

    # Define the required top-level keys
    required_top_level = {"type", "function"}
    if not isinstance(tool_definition, dict):
        raise ValueError("Tool definition must be a dictionary.")

    missing_keys = required_top_level - tool_definition.keys()
    if missing_keys:
        raise ValueError(f"Missing top-level keys: {missing_keys}")

    if tool_definition["type"] != "function":
        raise ValueError("The 'type' field must be 'function'.")

    function_details = tool_definition.get("function")
    if not isinstance(function_details, dict):
        raise ValueError("The 'function' field must be a dictionary.")

    # Required keys within 'function'
    required_function_keys = {"name", "description", "parameters"}
    missing_function_keys = required_function_keys - function_details.keys()
    if missing_function_keys:
        raise ValueError(f"Missing keys in 'function': {missing_function_keys}")

    # Validate 'name'
    if not isinstance(function_details["name"], str):
        raise ValueError("The 'name' field must be a string.")

    # Validate 'description'
    if not isinstance(function_details["description"], str):
        raise ValueError("The 'description' field must be a string.")

    # Validate 'parameters'
    parameters = function_details.get("parameters")
    if not isinstance(parameters, dict):
        raise ValueError("The 'parameters' field must be a dictionary.")

    # Check required keys in 'parameters'
    required_parameters_keys = {"type", "properties", "required", "additionalProperties"}
    missing_parameters_keys = required_parameters_keys - parameters.keys()
    if missing_parameters_keys:
        raise ValueError(f"Missing keys in 'parameters': {missing_parameters_keys}")

    if parameters["type"] != "object":
        raise ValueError("The 'type' field in 'parameters' must be 'object'.")

    # Validate 'properties'
    properties = parameters.get("properties")
    if not isinstance(properties, dict):
        raise ValueError("The 'properties' field must be a dictionary.")

    for prop, details in properties.items():
        if not isinstance(details, dict):
            raise ValueError(f"The details of property '{prop}' must be a dictionary.")
        if "type" not in details or "description" not in details:
            raise ValueError(f"Property '{prop}' must have 'type' and 'description' fields.")
        if not isinstance(details["type"], str):
            raise ValueError(f"The 'type' of property '{prop}' must be a string.")
        if not isinstance(details["description"], str):
            raise ValueError(f"The 'description' of property '{prop}' must be a string.")

    # Validate 'required'
    required_fields = parameters.get("required")
    if not isinstance(required_fields, list):
        raise ValueError("The 'required' field must be a list.")
    for field in required_fields:
        if field not in properties:
            raise ValueError(f"Required field '{field}' is not defined in 'properties'.")

    # Validate 'additionalProperties'
    if not isinstance(parameters["additionalProperties"], bool):
        raise ValueError("The 'additionalProperties' field must be a boolean.")

    # If all checks pass
    return True


def process_func_str(gen_flg: bool, tool_definition: str, func_str: str):
    """
    Parse the tool function to get correct code
    """
    
    # Decode escape sequences like \n and \"
    decoded_str = func_str.encode('utf-8').decode('unicode_escape')
    
    # Add decorator
    def_index = decoded_str.find("def ")
    if def_index != -1:
        if gen_flg:
            new_line = "from anyactions.base.decorators import *\n@generated_action\n" 
        else:
            new_line = "from anyactions.base.decorators import *\n@action\n"
        decoded_str = decoded_str[:def_index] + new_line + decoded_str[def_index:]
        
    # Add tool definition to the annotation
    if type(tool_definition) == str:
        decoded_str = '"""_tool_definition_\n[This is the tool definition passing to the LLM]\n' + tool_definition + '\n"""' + "\n\n" + decoded_str
    elif type(tool_definition) == dict:
        decoded_str = json.dumps(tool_definition, indent=4) + "\n\n" + decoded_str

    return decoded_str