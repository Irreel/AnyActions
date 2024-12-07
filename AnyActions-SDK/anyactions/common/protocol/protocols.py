"""Protocol for action execution status"""
ACTION_SUCCESS = b"success"
ACTION_FAILURE = b"failure"


"""Protocol for talking to the AnyActions server"""
class GetApiByProviderActionRequestBuilder:
    """
    Builder for GetApiByProviderActionRequest
    """
    def __init__(self):
        self.api_request = {
            "action_name": ""
        }

    def set_action(self, action: str) -> None:
        self.api_request["action_name"] = action

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
            "parameters": {
                "type": "function",
                "properties": {},
                "required": []
            },
            "registration_link": ""
        }

    def set_name(self, name: str) -> None:
        self.api_definition["name"] = name

    def set_action(self, action: str) -> None:
        self.api_definition["action"] = action

    def set_host(self, host: str) -> None:
        self.api_definition["host"] = host

    def set_endpoint(self, endpoint: str) -> None:
        self.api_definition["endpoint"] = endpoint

    def set_tool_function(self, tool_function: str) -> None:
        self.api_definition["tool_function"] = tool_function

    def add_parameter(self, name: str, param_type: str, description: str, required: bool = False) -> None:
        self.api_definition["parameters"]["properties"][name] = {
            "type": param_type,
            "description": description
        }
        if required:
            self.api_definition["parameters"]["required"].append(name)

    def set_registration_link(self, registration_link: str) -> None:
        self.api_definition["registration_link"] = registration_link

    def get(self) -> dict:
        return self.api_definition
