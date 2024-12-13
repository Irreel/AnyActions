from pydantic import BaseModel
from pydantic import Field
from typing import Dict, Optional


class ParamDetail(BaseModel):
    type: str
    description: str
    
class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, ParamDetail]
    required: list[str]
    additionalProperties: bool = False

class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters
    
class ToolDefinition(BaseModel):
    type: str = "function"
    function: Function
    
# Structured output does not support default values, thus put the raw response scheme here
class rawFunctionParameters(BaseModel):
    properties: Dict[str, ParamDetail]
    required: list[str]

class rawToolDefinition(BaseModel):
    function: Function
    
class rawResponseWithExec(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_function: str
    exec_sh: Optional[str]
    
class rawResponse(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_function: str