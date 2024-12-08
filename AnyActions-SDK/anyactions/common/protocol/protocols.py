"""Protocol for action execution status"""
ACTION_SUCCESS = b"success"
ACTION_FAILURE = b"failure"


"""Protocol for talking to the AnyActions server"""
from anyactions.common.procedure.local import function_to_json
from anyactions.common.db.validate import validate_tool_name

from typing import Callable, Literal

class GetApiByProviderActionRequestBuilder:
    """
    Builder for GetApiByProviderActionRequest
    """
    def __init__(self):
        self.api_request = {
            "action_name": ""
        }

    def set_action(self, action: str) -> None:
        self.api_request["action_name"] = validate_tool_name(action)

    def get(self) -> dict:
        return self.api_request


class SaveApiRequestBuilder:
    
    def __init__(self):
        self.api_definition = {
            "name": "",
            "action": "",
            "host": "",
            "endpoint": "",
            "tool_function": "",
            "tool_definition": {
                "type": "function",
                "properties": {},
                "required": []
            },
            "instruction": ""
        }
        
    def __call__(self, *args, **kwargs):
        self.set_by_callable(*args, **kwargs)
        
    def set_by_callable(self, func: Callable):
        assert isinstance(func, Callable)
        func_json = function_to_json(func)
        self.set_name(func_json["function"]["name"])
        self.set_action(func_json["function"]["name"])
        self.set_tool_function(inspect.getsource(func))
        self.set_tool_definition(func_json["function"]["parameters"])
        
        raise NotImplementedError

    def set_name(self, name: str) -> None:
        assert isinstance(name, str)
        self.api_definition["name"] = name

    def set_action(self, action: str) -> None:
        self.api_definition["action"] = validate_tool_name(action)

    def set_host(self, host: str) -> None:
        assert isinstance(host, str)
        self.api_definition["host"] = host

    def set_endpoint(self, endpoint: str) -> None:
        assert isinstance(endpoint, str)
        self.api_definition["endpoint"] = endpoint

    def set_tool_function(self, tool_function: str) -> None:
        self.api_definition["tool_function"] = tool_function
    
    def set_tool_definition(self, tool_definition: dict) -> None:
        self.api_definition["tool_definition"] = tool_definition

    def add_parameter(self, name: str, param_type: str, description: str, required: bool = False) -> None:
        assert isinstance(name, str)
        assert isinstance(param_type, str)
        assert isinstance(description, str)
        self.api_definition["tool_definition"]["properties"][name] = {
            "type": param_type,
            "description": description
        }
        if required:
            self.api_definition["tool_definition"]["required"].append(name)

    def set_instruction(self, instruction: str) -> None:
        assert isinstance(instruction, str)
        self.api_definition["instruction"] = instruction

    def get(self) -> dict:
        return self.api_definition


class CallbackApiRequestBuilder:
    def __init__(self):
        self.api_request = {
            "message": "",  
            "action_name": ""
        }

    def set_action(self, action: str) -> None:
        assert isinstance(action, str)
        self.api_request["action_name"] = validate_tool_name(action)
        
    def set_message(self, message: Literal[ACTION_SUCCESS, ACTION_FAILURE]) -> None:
        assert isinstance(message, ACTION_SUCCESS | ACTION_FAILURE)
        self.api_request["message"] = 1 if message == ACTION_SUCCESS else 0
    
    def get(self) -> dict:
        return self.api_request