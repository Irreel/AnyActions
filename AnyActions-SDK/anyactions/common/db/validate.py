"""
Type and format validation
"""
import re
from anyactions.common.types import *

def validate_action_name(action_name: str) -> bool:
    assert isinstance(action_name, str), "Action name must be a string"
    # Check for spaces
    if ' ' in action_name:
        raise ValueError("Action name cannot contain spaces")
    
    # Check for special characters except underscore
    if not re.match(r'^[a-zA-Z_]+$', action_name):
        raise ValueError("Action name can only contain letters and underscores")
    
    # TODO: Regular experssion
    
    return action_name.lower()

def check_function_syntax(tool_calling_function: str):
    """
    Validates if the input string is a legal Python function.
    
    Args:
        tool_calling_function (str): The string containing the Python function code
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        ValueError: If the code cannot be parsed as a valid Python function
    """
    import ast
    
    try:
        # Parse the string into an AST
        tree = ast.parse(tool_calling_function)
        
        # TODO: ignore the import statements
        # # Check if the parsed content contains exactly one function definition
        # if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        #     raise ValueError("Input must contain exactly one function definition")
            
        # Additional validation could be added here if needed
        return True
        
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse function: {str(e)}")
