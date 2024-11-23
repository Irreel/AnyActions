from ..aapi.utils import parse_tool_definition
from pathlib import Path
import json
        
# Example usage
tool_name = 'tool_calling_test.py'

try:
    tool_def = parse_tool_definition("./.actions", tool_name)
    print("Parsed Tool Definition:")
    print(json.dumps(tool_def, indent=4))
except ValueError as e:
    print(f"Error: {e}")