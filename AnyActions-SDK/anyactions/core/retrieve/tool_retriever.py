import json
from anyactions.common import *
from anyactions.common.constants import *
from anyactions.core.client.client import Client
from anyactions.core.client.request_status import RequestStatus

"""
Interact with the API to retrieve the tool and post-process the response
""" 

class Retriever:
    def __init__(self, client: Client, observer=False):
        self.client = client
        self.observer = observer
    
    def __call__(self, action_name: str) -> dict:
        """
        Retrieve the Tool Specification for a given action.

        :param action_name: The action name to retrieve the Tool Specification for.
        :return: A tuple containing the instruction, tool definition (json), and function body
        """
        if self.observer:
            print(f"Downloading {action_name}")
        status, response = self.client.get(DOWNLOAD_EP, query=self.get_request(action_name))
        if (status == RequestStatus.OK):
            return self.parse_response(response)
        elif (status == RequestStatus.NOT_FOUND):
            prompt = (
                f"'{action_name}' not found in AnyActions registry.\n"
                "Would you like to search for similar APIs online? [y/n]: "
            )
            if_gen = input(prompt).lower().strip()
            if if_gen == "y":
                # TODO: Fall back to generating with LLM
                # self.client.post("generate", query=self.get_request(action_name))
                raise NotImplementedError
            else:
                raise Exception(f"Tool {action_name} not found")
        elif status == RequestStatus.FORBIDDEN:
            raise Exception(f"Forbidden: Please check your API key for AnyActions")
        else:
            raise Exception(f"Failed to download {action_name} tool: {status}")
    
    def get_request(self, action_name: str) -> dict:
        builder = GetApiByProviderActionRequestBuilder()
        builder.set_action(action_name)
        return builder.get()
    
    def parse_response(self, response: dict):        
        if response["message"] == "Files retrieved successfully":
            
            gen_flg = response["files"]["gen_flg"]
            if gen_flg not in [0, 1]:
                if self.observer:
                    print(f"Invalid gen_flg value: {gen_flg}. Must be 0 or 1")
                return RequestStatus.INTERNAL_SERVER_ERROR
            gen_flg = bool(gen_flg)
            
            instruction = response["files"].get("registration_link", None)
            
            tool_def = response["files"]["tool_definition.json"]
            try:
                tool_def = json.loads(tool_def)
            except Exception as e:
                if self.observer:
                    print(f"Invalid tool definition json format: {e}")
                return RequestStatus.INTERNAL_SERVER_ERROR
            
            func_body = response["files"]["tools.py"]
            try:
                func_body = self.parse_func_str(gen_flg, tool_def, func_body)
            except Exception as e:
                if self.observer:
                    print(f"Invalid function body format: {e}")
                return RequestStatus.INTERNAL_SERVER_ERROR
            
            return (gen_flg, instruction, tool_def, func_body)
        else:
            return RequestStatus.INTERNAL_SERVER_ERROR
        


    def parse_func_str(self, gen_flg: bool, tool_definition: str|dict, func_str: str):
        """
        1. Parse the tool function to get correct code 
        2. Add tool definition
        3. Add decorator
        Args:
            gen_flg (bool): Whether the function is generated / not validated
            tool_definition (str|dict): Tool definition in string or dictionary
            func_str (str): Function code in string
        """
        
        # Decode escape sequences like \n and \"
        decoded_str = func_str.encode('utf-8').decode('unicode_escape')
        
        # Add decorator
        def_index = decoded_str.find("def ")
        if def_index != -1:
            if gen_flg:
                new_line = "from anyactions import generated_action\n\n@generated_action\n" 
            else:
                new_line = "from anyactions import action\n\n@action\n"
            decoded_str = decoded_str[:def_index] + new_line + decoded_str[def_index:]
            
        # Add tool definition to the annotation
        if type(tool_definition) == str:
            decoded_str = '"""_tool_definition_\n[This is the tool definition passing to the LLM]\n' + tool_definition + '\n"""' + "\n\n" + decoded_str
        elif type(tool_definition) == dict:
            decoded_str = '"""_tool_definition_\n' + json.dumps(tool_definition, indent=4) + '\n"""' + "\n\n" + decoded_str

        return decoded_str
        