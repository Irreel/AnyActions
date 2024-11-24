"""
Data schema to format LLM output
"""

from pydantic import BaseModel
from pydantic import Field


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
    
class rawResponse(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_calling_function: str
    exec_sh: Optional[str] = None
    
class rawResponseWithNoExec(BaseModel):
    instruction: str
    tool_definition: ToolDefinition
    tool_calling_function: str