"""
Type and format validation
"""
import re
from anyactions.common.protocol.types import *

def validate_tool_name(tool_name: str) -> bool:
    assert isinstance(tool_name, str)
    # Check for spaces
    if ' ' in tool_name:
        raise ValueError("Tool name cannot contain spaces")
    
    # Check for special characters except underscore
    if not re.match(r'^[a-zA-Z_]+$', tool_name):
        raise ValueError("Tool name can only contain letters and underscores")
    
    # TODO: Regular experssion
    
    return tool_name.lower()

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
