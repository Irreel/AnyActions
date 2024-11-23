"""
Task:
- Check if the tool definition subject to OpenAI tool calling format
- Check if the generated function body is a valid Python function
"""

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

