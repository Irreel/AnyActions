import os
import json
import inspect
import importlib.util
from typing import List, Callable, Any
from .exception.anyactions_exceptions import *

def create_local_tools_dir(api_dir_path, observer=False):
    """Create local directory for storing tools"""
    if not os.path.exists(api_dir_path):
        os.makedirs(api_dir_path)
        os.makedirs(os.path.join(api_dir_path, '.api_keys'))
        with open(os.path.join(api_dir_path, '.config'), 'w') as f:
            pass
        if observer:
            print(f"Local tools directory created: {api_dir_path}")
        return True
    else:
        if observer:
            print(f"Local tools directory already exists: {api_dir_path}")
        return False
    
def check_local_tool_legit(api_dir_path, tool_name, observer=False):
    """Check if local tools directory exists and with api keys"""
    assert os.path.exists(api_dir_path), LocalToolException(f"Local tools directory does not exist: {api_dir_path}. Check if ActionHub is initialized correctly.")
    
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    assert os.path.exists(tool_path), LocalToolException(f"Local tool does not exist: {tool_path}. Check if the tool is registered in ActionHub.")
    
    # Check if tool definition is valid
    tool_def = parse_tool_definition(api_dir_path, tool_name)
    
    # Check tool name consistency
    assert tool_def.get("function", {}).get("name") == tool_name, LocalToolException(f"Tool name inconsistency: Check if tool name in tool_definition is consistent with the tool name {tool_def.get('function', {}).get('name')} VS {tool_name}")
    
    # Check if api key is needed
    try:
        func = load_callable(tool_name, tool_path)
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    if "api_key" in signature.parameters:
        api_key_param = signature.parameters["api_key"]
        if api_key_param.default == inspect._empty:
            assert check_local_api_key(api_dir_path, tool_name, observer), LocalToolException(f"API key is required for {tool_name}. Please add an API key.")
    
    # Check if dependencies are satisfied
    
    # raise NotImplementedError("Not implemented")
    return True

def check_local_api_key(api_dir_path, tool_name, observer=False):
    """Check if api key is needed and exists"""
    api_key_path = os.path.join(api_dir_path, '.api_keys', f"{tool_name.upper()}_KEY")
    try:
        assert os.path.exists(api_key_path)
        return True
    except AssertionError:
        return False
    
def check_tool_decorator(tool_function: Callable[..., Any]) -> dict:
    """
    Check if a tool function has specific decorators.
    
    Args:
        tool_function: The function to check for decorators
        
    Returns:
        dict: Dictionary containing decorator information
        {
            'has_decorators': bool,
            'decorators': list of decorator names,
            'original_function': name of the original function
        }
    """
    result = {
        'has_decorators': False,
        'decorators': [],
        'original_function': tool_function.__name__
    }
    
    if hasattr(tool_function, '__wrapped__'):
        result['has_decorators'] = True
        current_func = tool_function
        
        # Walk through all decorators
        while hasattr(current_func, '__wrapped__'):
            result['decorators'].append(current_func.__name__)
            current_func = current_func.__wrapped__
            
        result['original_function'] = current_func.__name__
        
    return result    

def get_all_local_tool_names(api_dir_path: str, observer=False) -> List[str]:
    """Load names of existing tools from local directory"""
    assert os.path.exists(api_dir_path), LocalToolException(f"Local tools directory does not exist: {api_dir_path}. Check if ActionHub is initialized correctly.")
    
    tool_list = [] 
    # Load local tools
    for file in os.listdir(api_dir_path):
        if file.endswith('.py'):
            tool_list.append(file[:-3])
    if observer:
        print(f"{len(tool_list)} local tools loaded")
    return tool_list

def get_local_tool_definition(api_dir_path: str, tool_name: str, observer=False):
    """Load a single local tool from local directory"""
    check_local_tool_legit(api_dir_path, tool_name, observer)
    
    tool_definition = parse_tool_definition(api_dir_path, tool_name)
    if observer:
        print(f"Local tool definition loaded: {tool_definition}")
    return tool_definition

def get_local_api_key(api_dir_path: str, tool_name: str, observer=False):
    """Get the api key for a local tool"""
    api_key_path = os.path.join(api_dir_path, '.api_keys', f"{tool_name.upper()}_KEY")
    assert os.path.exists(api_key_path), LocalToolException(f"API key for {tool_name} not found in {api_key_path}. Please check if the API key file exists.")
    
    with open(api_key_path, 'r') as f:
        api_key = f.read()
    return api_key
    
def load_callable(action_name: str, file_path: str) -> Callable:
    """Load a local function from a file"""
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location(action_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Get the main function (assumed to be named the same as the action_name)
        tool_function = getattr(module, action_name)
        return tool_function
    except Exception as e:
        raise LocalToolException(f"Failed to load function {action_name} from {file_path}: {e}")
    
def parse_tool_definition(local_env_path: str, tool_name: str) -> dict:
    """
    Parses the _tool_definition_ from the specified Python file.

    Args:
        local_env_path (Path): The path to the local environment directory.
        tool_name (str): The name of the tool file (e.g., 'tool_function.py').

    Returns:
        dict: The parsed tool definition.
    """
    
    tool_path = os.path.join(local_env_path, f"{tool_name}.py")
    
    try:
        with open(tool_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Tool calling function {tool_name} not found at path: {tool_path}")

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
        return function_to_json(load_callable(tool_name, tool_path))

    return tool_definition

def function_to_json(func: Callable, skip_api_key=True) -> dict:
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
        
    if skip_api_key:
        parameters.pop("api_key", None)

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
                "additionalProperties": False
            },
        },
    }

def write_local_tool(api_dir_path: str, tool_definition: dict, tool_func: str, exec_sh=None):
    """
    Write tool function to local environment. Might execute shell commands in the future.

    Args:
        api_dir_path (str): Path to the directory storing API configurations and tools.
        tool_definition (dict): Tool definition in OpenAI format.
        tool_func (str): Function code as a string.
        exec_sh (str, optional): Shell commands to execute. Defaults to None.
    """
    
    tool_name = tool_definition.get("name") or tool_definition.get("function").get("name") # Anthropic schema Or OpenAI schema
    tool_file_path = os.path.join(api_dir_path, f"{tool_name}.py")

    try:
        with open(tool_file_path, 'w', encoding='utf-8') as f:
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
            
            # Write function body with proper indentation and line breaks
            f.write(tool_func)

        if exec_sh:
            # Execute any shell commands if provided
            subprocess.run(exec_sh, shell=True, check=True)
            
    except Exception as e:
        raise LocalToolException(f"Failed to write tool to {tool_file_path}: {e}")
