import os
import json
import requests
from typing import List


from .utils import create_inter_api_key, definition
from .db_tmp import db_index, db, tool_name_to_index

class Hub:
    
    def __init__(self, api_key, environment_context={}, api_file_path='./'):
                
        self.environment_context = environment_context
        self.user = {
            "hub_api_key": api_key,
        }
        
        # Debug print statements
        print(f"Initializing aapi with environment_context: {environment_context}")
        # print(f"API key set: {'Yes' if api_key else 'No'}")
        
        # Maintain 3rd party API Keys 
        # ##TODO: save the API at serverside
        self.api_file_path = os.path.join(api_file_path, '.env_api_key')
                    
    def tools(self, tool_list: List) -> List[dict]:
        self.definition_list = definition(tool_list)
        return self.definition_list
        
    
    def verification(self, api_name):
        """_summary_
        TODO: Currently it keeps 3rd party API keys locally

        This function checks if an API key is needed for the specified API, and if so,
        attempts to retrieve from local api index or create one. It handles both APIs that require keys and
        those that don't.

        Args:
            api_name (str): The name of the API to verify.

        Returns:
            tuple: A tuple containing:
                - status (bool): True if verification was successful, False otherwise.
                - provider_name (str): The name of the API provider.
                - action_name (str): The name of the specific API action.
                - inter_api_key (str or None): The API key if required, None otherwise.

        Raises:
            ValueError: If creation of a required API key fails.
        """
        
        # Assume all the api name is formatted in upperletters
        legal_api_name = api_name.upper() 
        
        # Check if it needs api key verification
        provider_name, action_name = legal_api_name.split("_")[:2]
        if db[provider_name][action_name]["api_key_flg"] == 0:
            return True, provider_name, action_name, None
        
        ###### If it needs api key verification
        # Access local API key
        if not os.path.exists(self.api_file_path):
            api_key_found = False
        else:
            with open(self.api_file_path, 'r') as f:
                lines = f.readlines()
                # Check if the API key for the legal_api_name exists in the file
                api_key_found = False
                for line in lines:
                    if line.strip().startswith(f"ACTION_{legal_api_name}_KEY"):
                        api_key_found = True
                        # Extract the inter_api_key from the line
                        inter_api_key = line.strip().split('=')[1].strip().strip("'")
                        break
                    
        ###### If api key is not found
        if not api_key_found:
            with open(self.api_file_path, 'w') as f:
                status, inter_api_key = create_inter_api_key(legal_api_name, self.api_file_path, self.user)
                if status:
                    f.write(f"ACTION_{legal_api_name}_KEY = '{inter_api_key}'\n")
                else:
                    raise ValueError(f"Failed to create {legal_api_name} key")          
        
        return True, provider_name, action_name, inter_api_key
        
          
    def _act(self, api_name, input_params, entrypoint_cache=True):
        
        assert isinstance(api_name, str)
        
        # Format input params
        match input_params:
            case dict():
                pass
            case str():
                try:
                    input_params = json.loads(input_params)
                except json.JSONDecodeError as e:
                    print(f"Error decoding input parameters: {e}")
                    raise ValueError("Invalid JSON string provided for input_params")
            case list():
                raise NotImplementedError
            case tuple():
                raise NotImplementedError
            case _:
                raise ValueError("Unsupported input parameter type")
        
        # TODO: Search target API if api_name is not specified
        if api_name not in db_index:
            # TODO: Search a relevant entrypoint in the database
            search_result = ''
            
            # TODO: Not sure about this feature: save/append the called function into local file??
            
            raise NotImplementedError
        
        else:
            # Specify an api_name
            status, provider_name, action_name, inter_api_key = self.verification(api_name)
            
            # Get the calling specification
            request_type = db[provider_name][action_name]["request"]
            entrypoint = db[provider_name][action_name]["entrypoint"]
            input_schema = db[provider_name][action_name]["input_schema"]
            config_params = db[provider_name][action_name].get('config_params', None)
            output_schema = db[provider_name][action_name]["output_schema"]
            
            # TODO: Consider required params and optional params
            
            # This is the params passing to the request, which can be different than user input params
            pass_params = {**input_params, **config_params} if config_params else input_params
            
            if inter_api_key:
                pass_params["api_key"] = inter_api_key
            
            
        ######
        # Execute the function
        #####
        
        # TODO: other request types
        
        if request_type == "GET":
            try:
                response = requests.get(entrypoint, params=pass_params)
            except Exception as e:
                raise Exception(f"{api_name} {request_type} request error")
                # return ?
                
            data = response.json()
        
        return data, output_schema
    

    def act(self, response_object):
        # TODO: rename to response_act ?
        """_summary_
        Support object type: 
            - openai.types.chat.chat_completion.ChatCompletion
            - anthropic.types.message.Message
        """
        
        #######
        # Parse the response object
        #######
        
        # print(type(response_object)) # <class 'anthropic.types.message.Message'>
        # print(isinstance(response_object, dict)) # False 
        
        if isinstance(response_object, list):
            if len(response_object) == 1:
                response_object = response_object[0]
            else:
                # This is useful for LLM responses which include a tool usage request with other text response 
                for entry in response_object:
                    # Assume there is only one tool usage request in model responses
                    try:
                        response, output_schema = self.act(entry)
                        # break once it found the tool usage request
                        break
                    except:
                        raise Exception("Unsupported response object type")
                return response, output_schema
            
        else:
            # TODO: find a better way to identify the object without installing 3rd party package. 
            # (Solution 1: some packages re-write these object definition in their library, like langchain, litellm etc.)
            response_object = dict(response_object)
            
        # Check if it is ChatCompletion object in openai
        if (isinstance(response_object, dict) and
            'choices' in response_object and
            isinstance(response_object['choices'], list) and
            len(response_object['choices']) > 0 and
            'message' in response_object['choices'][0]):
            
            # Extract the message from the first choice
            message = response_object['choices'][0]['message']
            
            # Check if there are tool calls in the message
            if 'tool_calls' in message and message['tool_calls'] is not None:
                for tool_call in message['tool_calls']:
                    if tool_call.get('type') == 'function':
                        function_name = tool_call['function']['name']
                        function_args = json.loads(tool_call['function']['arguments'])
                        
                        print(f"Function to call: {function_name}")
                        print(f"Arguments: {function_args}")
            else:
                # If there are no tool calls, just print the content
                print(f"No tool calls. Model response: {message.get('content')}")
        
        # if it is ChatCompletionMessage object from OpenAI
        # ...
        
        # if it is ChatCompletionMessageToolCall object from OpenAI
        # ...
        
        # Check if it is a ToolUseBlock-like object in claude 
        elif (isinstance(response_object, dict) and
            'name' in response_object and
            'input' in response_object):
                function_name = response_object['name']
                function_args = response_object['input']
      
        
        # if it is <class 'anthropic.types.message.Message'> in claude
        elif (isinstance(response_object, dict) and
            'content' in response_object and
            'stop_reason' in response_object):
            
            content = response_object['content']
            
            if response_object['stop_reason'] == 'tool_use':
                for item in content:
                    # TODO: find a better way to identify these object
                    item = dict(item)
                    if item['type'] == 'text':
                        pass
                    elif item['type'] == 'tool_use':
                        function_name = item['name']
                        function_args = item['input']
                        
                        print(f"  Tool name: {item['name']}")
                        print(f"  Tool input: {json.dumps(item['input'], indent=2)}")
            else:
                print(f"No tool calls. Model response: {content[0].get('text')}")
            
        else:
            raise Exception("Unsupported response object type")
        
        
        ######
        # TODO: Handle error response from model
        ######
        #
        
        #######
        # Get action function from db
        #######
        legal_api_name= tool_name_to_index[function_name]
        
        response, output_schema = self._act(legal_api_name, function_args)
        
        ######
        # TODO: Handle error response from 3rd party api like invalid api key, expired api key etc.
        ######
        if 'error' in response: # claude error response
            raise Exception(f"Error: {response['error']}")
        
        return response, output_schema
        
        
# class Actions:
    
#     def __init__(self, name_list):
#         raise NotImplementedError

    

