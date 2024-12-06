import os
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
    """Check if local tools directory exists and with valid api keys"""
    assert os.path.exists(api_dir_path), LocalToolException(f"Local tools directory does not exist: {api_dir_path}. Check if ActionHub is initialized correctly.")
    
    tool_path = os.path.join(api_dir_path, f"{tool_name}.py")
    assert os.path.exists(tool_path), LocalToolException(f"Local tool does not exist: {tool_path}. Check if the tool is registered in ActionHub.")
    
    # Check if api is available
    
    # return os.path.exists(api_dir_path)
    raise NotImplementedError("Not implemented")

def load_all_local_tool_names(api_dir_path, observer=False):
    """Load existing tools from local directory"""
    tool_list = []  # Reset tool list
    
    assert os.path.exists(api_dir_path), f"Local tools directory does not exist: {api_dir_path}"
    
    # Load local tools
    for file in os.listdir(api_dir_path):
        if file.endswith('.py'):
            tool_list.append(file[:-3])
    if observer:
        print(f"{len(tool_list)} local tools loaded")
    return tool_list

def load_local_tool_definition(api_dir_path, tool_name, observer=False):
    """Load a single local tool from local directory"""
    check_local_tool_legit(api_dir_path, tool_name, observer)
    
    tool_definition = parse_tool_definition(api_dir_path, tool_name)
    if observer:
        print(f"Local tool definition loaded: {tool_definition}")
    return tool_definition
    
def parse_tool_definition(local_env_path, tool_name: str) -> dict:
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
