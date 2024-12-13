"""
Data schema to format LLM output
"""

from pydantic import BaseModel
from pydantic import Field
from typing import Dict, Optional


class ParamDetail(BaseModel):
    type: str
    description: str
    
class FunctionParameters(BaseModel):
    properties: Dict[str, ParamDetail]
    required: list[str]

class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters

class ToolDefinition(BaseModel):
    function: Function
    
class formattedFunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, ParamDetail]
    required: list[str]
    additionalProperties: bool = False

class formattedToolDefinition(BaseModel):
    type: str = "function"
    function: Function
    
class rawResponse(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_function: str
    exec_sh: Optional[str]
    
class rawResponseWithNoExec(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_function: str
    
# class rawResponseWithNoExec_test(BaseModel):
#     instruction: str
#     tool_definition: {
#         "type": "function",
#         "function": {
#             Function
#         }
#     }
#     tool_function: str

def check_name_consistency(tool_name: str, generatedApiSpec: dict):
    generatedApiSpec['tool_definition']['function']['name'] = tool_name
    
    func_body = generatedApiSpec['tool_function']
    
    if func_body.find(tool_name) == -1:
        # Replace function name in function body
        func_lines = func_body.split('\n')
        for i, line in enumerate(func_lines):
            if line.startswith('def '):
                func_lines[i] = line.replace(line[4:line.find('(')], tool_name)
                break
        generatedApiSpec['tool_function'] = '\n'.join(func_lines)
    
    return generatedApiSpec