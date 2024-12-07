from pydantic import BaseModel
from pydantic import Field
from typing import Dict, Optional


class ParamDetail(BaseModel):
    type: str
    description: str
    
class rawFunctionParameters(BaseModel):
    properties: Dict[str, ParamDetail]
    required: list[str]
    
class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, ParamDetail]
    required: list[str]
    additionalProperties: bool = False

class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters

class rawToolDefinition(BaseModel):
    function: Function
    
class ToolDefinition(BaseModel):
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