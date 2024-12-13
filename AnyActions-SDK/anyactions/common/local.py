import os
import json
import inspect
import importlib.util
from typing import List, Callable, Any
from anyactions.common.exception.anyactions_exceptions import *

def write_local_tool(api_dir_path: str, tool_definition: dict, tool_func: str, exec_sh=None) -> None:
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

def read_local_tool(api_dir_path: str, tool_name: str) -> dict:
    """Read a local tool from local directory"""
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    
    with open(tool_path, 'r', encoding='utf-8') as f:
        return f.read()
    
    tool_definition = read_tool_definition(api_dir_path, tool_name)
    try:
        tool_func = get_tool_callable(tool_name, tool_path)
        signature = inspect.signature(tool_func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )
    
    return {
        "tool_definition": tool_definition,
        "tool_func": tool_func,
        "status": None,
    }

######
# Local tool directory
######    
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

######
# Validation for local tool calling
######    
def check_local_tool_legit(api_dir_path, tool_name, observer=False):
    """Check if local tools directory exists and with api keys"""
    assert check_local_tools_dir_exists(api_dir_path)
    assert check_local_tool_exists(api_dir_path, tool_name)
    
    # Check if tool definition is valid
    tool_def = read_tool_definition(api_dir_path, tool_name)
    
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    # Check tool name consistency
    assert tool_def.get("function", {}).get("name") == tool_name, LocalToolException(f"Tool name inconsistency: Check {tool_path} if tool name in tool_definition is consistent with the tool name {tool_def.get('function', {}).get('name')} VS file name{tool_name}")
    
    # Check if api key is needed
    try:
        func = get_tool_callable(tool_name, tool_path)
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    if "api_key" in signature.parameters:
        api_key_param = signature.parameters["api_key"]
        if api_key_param.default == inspect._empty:
            assert check_local_api_key_exists(api_dir_path, tool_name, observer), LocalToolException(f"API key is required for {tool_name}. Please add an API key.")
    
    # TODO:Check if dependencies are satisfied
    
    return True

def check_local_tools_dir_exists(api_dir_path: str, observer=False):
    """Check if local tools directory exists"""
    assert os.path.exists(api_dir_path), LocalToolException(f"Local tools directory does not exist: {api_dir_path}. Check if ActionHub is initialized correctly.")
    return True

def check_local_tool_exists(api_dir_path, tool_name, observer=False):
    """Check if local tool exists"""
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    assert os.path.exists(tool_path), LocalToolException(f"Local tool does not exist: {tool_path}. Check if the tool is registered in ActionHub.")
    return True

def check_local_api_key_exists(api_dir_path, tool_name, observer=False):
    """Check if api key exists"""
    api_key_path = os.path.join(api_dir_path, '.api_keys', f"{tool_name.upper()}_KEY")
    if not os.path.exists(api_key_path):
        return False   
    with open(api_key_path, 'r') as f:
        content = f.read().strip()    
    return bool(content)

def check_local_tool_auth_method(api_dir_path, tool_name, observer=False):
    """Currently, check if the tool needs api key
    
    Returns:
        int: 0 if no api_key parameter
             1 if api_key is required
             2 if api_key is optional
    """
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    tool_func = get_tool_callable(tool_name, tool_path)
    signature = inspect.signature(tool_func)
    
    if "api_key" not in signature.parameters:
        return 0
        
    api_key_param = signature.parameters["api_key"]
    return 1 if api_key_param.default == inspect._empty else 2
    
def check_tool_decorator(tool_function: Callable[..., Any], target_decorator: str, observer=False) -> dict:
    """Check if a tool function has specific decorators.

    Args:
        tool_function: The function to check for decorators
        target_decorator: The decorator name to check for
        observer: Flag to enable logging, defaults to False

    Returns:
        dict: Dictionary containing decorator information with the following keys:
            - has_decorators: bool indicating if any decorators are present
            - decorators: list of decorator names
            - original_function: name of the original function
    """
    assert target_decorator in ['action', 'generated_action']
    
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
        
    if target_decorator in result['decorators']:
        return True
    else:
        return False

######
# Read/Get local tools list
######    
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
    
    tool_definition = read_tool_definition(api_dir_path, tool_name)
    if observer:
        print(f"Local tool definition loaded: {tool_definition}")
    return tool_definition

def get_local_tool_function_params(api_dir_path: str, tool_name: str, observer=False):
    """Get the parameters of a local tool function"""
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    try:
        # Get the function using get_tool_callable
        tool_func = get_tool_callable(tool_name, tool_path)
        # Get the function signature
        signature = inspect.signature(tool_func)
        # Convert parameters to dictionary
        params = {
            name: {
                'annotation': str(param.annotation) if param.annotation != inspect._empty else None,
                'default': param.default if param.default != inspect._empty else None
            }
            for name, param in signature.parameters.items()
        }
        if observer:
            print(f"Function parameters for {tool_name}: {params}")
        return params
    except Exception as e:
        raise LocalToolException(f"Failed to get function parameters for {tool_name}: {e}")

def get_local_api_key(api_dir_path: str, tool_name: str, observer=False):
    """Get the api key for a local tool"""
    api_key_path = os.path.join(api_dir_path, '.api_keys', f"{tool_name.upper()}_KEY")
    assert os.path.exists(api_key_path), LocalToolException(f"API key for {tool_name} not found in {api_key_path}. Please check if the API key file exists.")
    
    with open(api_key_path, 'r') as f:
        api_key = f.read()
    return api_key
    
def get_tool_callable(action_name: str, file_path: str) -> Callable:
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

######
# Read other tool attributes. Input is tool name and tool path string
######    
def read_tool_definition(api_dir_path: str, tool_name: str) -> dict:
    """
    Parses the _tool_definition_ from the specified Python file based on AnyActions schema.

    Args:
        api_dir_path (Path): The path to the local environment directory.
        tool_name (str): The name of the tool file (e.g., 'tool_function.py').

    Returns:
        dict: The parsed tool definition.
    """
    
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    
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
        return function_to_json(get_tool_callable(tool_name, tool_path))

    return tool_definition

def read_tool_decorators(api_dir_path: str, tool_name: str) -> List[str]:
    """Read the decorators of a tool"""
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    
    tool_func = get_tool_callable(tool_name, tool_path)
    
    decorators = []
    if hasattr(tool_func, '__wrapped__'):
        current_func = tool_func

        # Walk through all decorators
        while hasattr(current_func, '__wrapped__'):
            decorators.append(current_func.__name__)
            current_func = current_func.__wrapped__
            
    return decorators  

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

######
# Update local tool
######    
def validate_local_tool(api_dir_path: str, tool_name: str, observer=False):
    """Validate the usable status of a tool"""
    try:
        tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
        with open(tool_path, 'r', encoding='utf-8') as f:
            file = f.read()
        
        # Split content into lines to handle updates
        lines = file.splitlines()
        updated_lines = []
        
        # Use enumerate to get both index and line
        for i, line in enumerate(lines):
            # Handle anyactions import
            if line.startswith('from anyactions import'):
                parts = line.split('import')
                imports = parts[1].replace('generated_action', 'action')
                updated_line = f"{parts[0]}import{imports}"
                updated_lines.append(updated_line)
                
            # Handle decorator replacement
            elif line.strip() == '@generated_action' and i + 1 < len(lines) and lines[i + 1].strip().startswith('def '):
                updated_lines.append('@action')
            else:
                updated_lines.append(line)
                
        updated_file = '\n'.join(updated_lines)
        
        # Write back the updated content
        with open(tool_path, 'w', encoding='utf-8') as f:
            f.write(updated_file)
            
        return True
        
    except Exception as e:
        if observer:
            print(f"Failed to validate tool {tool_name}: {e}")
        return False
