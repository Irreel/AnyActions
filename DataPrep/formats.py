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