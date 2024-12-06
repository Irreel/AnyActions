from anyactions.core.client import Client, RequestStatus
# import anyactions.common.procedure.actions as actions

import os
import json
import requests
from getpass import getpass
from dotenv import load_dotenv
from typing import List, Dict, Union, Optional

from anyactions.core.abstract import *
from anyactions.common.local import *

from .utils import create_inter_api_key

from anyactions.common.base import ToolDefinition

from .utils import add_tool_to_local, parse_func_str

# TODO: replace this mock module
# from .db_tmp import db_index, db, tool_name_to_index

from anyactions.common.constants import LOCAL_ENV_PATH

class ActionHub:
    
    def __init__(self, env={}, api_dir_path=LOCAL_ENV_PATH):
        """
        Initialize the ActionHub class which manages tool loading, API key handling, and tool execution.
        
        Args:
            env (dict, optional): Environment variables for LLM configuration and user machine settings. 
            api_dir_path (str, optional): Path to the directory storing API configurations and tools.
                
        Directory Structure Created:
            - api_dir_path/
                - .api_keys/     # Directory storing API keys for different tools
                - .config        # Configuration file for the hub
                - *.py          # Python files containing tool definitions
                
        Attributes:
            env (dict): Stored environment variables
            base_url (str): Base URL for AWS Gateway API loaded from environment
            user (dict): User credentials including API key
            # TODO: resolved_endpoint (dict): Cache for resolved API endpoints
            tool_list (List[str]): List of locally available tool names
            api_dir_path (str): Path to API directory
            api_keys_path (str): Path to API keys directory
            api_config_path (str): Path to config file
        """
        self.env = env
        
        load_dotenv()
        self.base_url = os.environ["AWS_GATEWAY_BASE_URL"]
        self.user = {
            "api_key": os.environ["AWS_GATEWAY_API_KEY"],
        }
        
        self.resolved_endpoint = {}
        
        ## Local tool loading
        self.tool_list: List[str] = []
        # This local tool list includes the tools that have been stored in the local file, notice this does not mean their api keys always work
        
        if os.path.exists(api_dir_path):
            # Load local tools
            self.tool_list = load_all_local_tool_names(api_dir_path)
        else:
            create_local_tools_dir(api_dir_path)
        
        ## API Key Initialization
        self.api_dir_path = api_dir_path
        self.api_keys_path = os.path.join(api_dir_path, '.api_keys')
        self.api_config_path = os.path.join(api_dir_path, '.config')
        
    def _list_tools(self):
        return self.tool_list
        
    def tools(self, tool_list: List[str | dict]) -> List[dict]:
        """Initialize a set of tool definitions available to LLM, including loading existing local tools and setting up new tools
        
        Args:
            tool_list (List): List of tool names or tool definitions

        Raises:
            ValueError: tool definition parsing failed

        Returns:
            List[dict]: tool definition list
        """
        
        definition_list = []
        for i in tool_list: 
            if isinstance(i, str):
                # Load tools from local
                if i in self.tool_list:
                    try:
                        definition_list.append(load_local_tool_definition(self.api_dir_path, i))
                    except Exception as e:
                        raise Exception(f"{i} Parse tool definition failed. Please check if {self.api_dir_path}{i}.py is valid: {e}")
                else:
                    # If not existed in local env, setup new tools
                    response = self._setup_tool(i)
                    definition_list.append(response)

            elif isinstance(i, dict):
                try:
                    tool_def = ToolDefinition(**i)
                except Exception as e:
                    print(f"Invalid OpenAI tool definition format: {e}")
                    print("Still added")

                definition_list.append(i)
            
            else:
                raise ValueError("Tool list should be a list of strings or dictionaries")
        
        return definition_list
        
    def _setup_tool(self, tool_name):
        
        # TODO: check dependencies - warning before the execution stage?
        # instruction, tool_def, func_body = get_tool_calling_function(tool_name)
        
        client = Client(self.base_url, self.user["api_key"])

        status, response = client.download(tool_name)
        if status == RequestStatus.OK:
            instruction, tool_def, func_body = response
            func_body = parse_func_str(False, tool_def, func_body)
            tool_def = json.loads(tool_def)
        elif status == RequestStatus.FORBIDDEN:
            raise Exception(f"Forbidden: Please check your API key for AnyActions")
        else:
            raise Exception(f"Failed to download {tool_name} tool: {status}")
            
        try:
            add_tool_to_local(self.api_dir_path, tool_def, func_body)
            
            # TODO: how to determine if API is optional, read from params?
            if instruction:
                print(f"You can set up the API key here: {instruction}\n")
                api_key = getpass("Paste your API key here:")
                if api_key:
                    # TODO: check if the api_key is already existed
                    with open(os.path.join(self.api_dir_path, '.api_keys', f"ACTION_{tool_name.upper()}_KEY"), 'w') as f:
                        f.write(f"ACTION_{tool_name.upper()}_KEY = '{api_key}'\n")
                else:
                    raise ValueError("API key is required")
            
            print(f"{tool_name}.py added")            
            return tool_def
        
        except Exception as e:
            raise ValueError(f"Failed to set up {tool_name} tool in local environment: {e}")
    
        
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
        
        # TODO: legal format of api name is just tentative. Assume all the api name is formatted in upperletters
        legal_api_name = api_name.upper()   
        provider_name, action_name = legal_api_name.split("_", maxsplit=1)
        
        # Check if endpoint url is customized
        endpoint = db[provider_name][action_name]["endpoint"]
        endpoint_params = db[provider_name][action_name].get('endpoint_params', None)
        
        # TODO: if we should stored all the endpoint params in a local file?
        
        if len(endpoint_params) > 0:
            endpoint_params = dict(db[provider_name][action_name]['endpoint_params'])
            endpoint_params_dict = {}
            for param in endpoint_params.items():
                x = input(f"\nPlease enter {param[0]} to set up {api_name} API ({param[1]}):")
                if x:
                    endpoint_params_dict[param[0]] = x
                else:
                    raise ValueError(f"\nPlease enter {param[0]} to set up {api_name} API. Read {provider_name} documentation for parameter details: {db[provider_name][action_name]['documentation']}")
            try:
                self.resolved_endpoint[legal_api_name] = endpoint.format(**endpoint_params_dict)
            except:
                raise ValueError(f"Failed to resolve endpoint params for {api_name}")
                return False, provider_name, action_name, None
        
        # Check if it needs api key verification  
        api_key_flg = int(db[provider_name][action_name]["api_key_flg"])
        if api_key_flg == 0:
            # No api key required
            return True, provider_name, action_name, None
        
        # If api key verification is required or optional
        # Try to access local API key, if not found, create one; if key is optional, still create a null string
        
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
                    
        if not api_key_found:
            status = False
            if api_key_flg == 1:
                # If local API key is not found
                status, inter_api_key = create_inter_api_key(legal_api_name, self.api_file_path, self.user, api_key_flg=api_key_flg)  
            elif api_key_flg == 2:
                # If api key is optional, still create a null string
                print(f"API key is optional for {legal_api_name}. Do not use key temporarily.")
                inter_api_key = ''
                status = True   
    
            if status:
                with open(self.api_file_path, 'w') as f:
                    f.write(f"ACTION_{legal_api_name}_KEY = '{inter_api_key}'\n")
            else:
                raise ValueError(f"Failed to create {legal_api_name} key")  
        
        return True, provider_name, action_name, inter_api_key
           
    @deprecated
    def _act_local(self, api_name, input_params, endpoint_cache=True):

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
            # TODO: Search a relevant endpoint in the database
            search_result = ''
            
            # TODO: Not sure about this feature: save/append the called function into local file??
            
            raise NotImplementedError
        
        else:
            # Specify an api_name
            status, provider_name, action_name, inter_api_key = self.verification(api_name)
            
            # Get the calling specification
            request_type = db[provider_name][action_name]["request"]
            endpoint = db[provider_name][action_name]["endpoint"] 
            endpoint_params = db[provider_name][action_name].get('endpoint_params', None)
            if endpoint_params:
                endpoint = self.resolved_endpoint[api_name]
            input_schema = db[provider_name][action_name]["input_schema"]
            config_params = db[provider_name][action_name].get('config_params', None)
            output_schema = db[provider_name][action_name]["output_schema"]
            
            # TODO: Consider required params and optional params
            
            # This is the params passing to the request, which can be different than user input params
            pass_params = {**input_params, **config_params} if config_params else input_params
            
            # TODO: Add more calling authentication methods
            if inter_api_key:
                pass_params["api_key"] = inter_api_key
            
            
        ######
        # Execute the function
        #####
        
        # TODO: other request types
        
        if request_type == "GET":
            try:
                response = requests.get(endpoint, params=pass_params)
            except Exception as e:
                # print(f"{api_name} {request_type} request error: {e}")
                raise Exception(e)
                
            data = response.json()
        
        return data, output_schema
    
    def _act(self, api_name, input_params, endpoint_cache=True):
        
        from .server_tmp import google_search_tool
        
        if api_name in db_index:    
            if api_name == "GOOGLE_SEARCH":
                return google_search_tool(input_params['q'], None) # TODO
        else:
            raise NotImplementedError

    def act(self, response_object, observer=False):
        """Process and execute tool/function calls from LLM response objects.
        
        This method handles different types of response objects from various LLM providers
        (like OpenAI and Anthropic) and executes the requested tool/function calls.
        
        Args:
            response_object (Union[dict, list]): The response object from an LLM. Supported types:
                - openai.types.chat.chat_completion.ChatCompletion
                - anthropic.types.message.Message
                - List containing either of the above
            observer (bool, optional): If True, returns the tool being called and its arguments
                instead of executing the call. Defaults to False.
                
        Returns:
            Tuple[Any, Optional[dict]]: A tuple containing:
                - response: The result from executing the tool/function call
                - output_schema: Schema definition for the response format, or None if no schema exists
                
        Raises:
            Exception: If the response object type is unsupported or if there are errors in
                tool execution or API responses
                
        Examples:
            >>> hub = ActionHub()
            >>> response = llm.chat(...)  # Get response from LLM
            >>> result, schema = hub.act(response)
        """
        
        #######
        # Parse the response object
        # TODO: Just a very naive and temporary solution for parsing different response objects. Gonna replace it with a more robust one.
        #######
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
                print(f"\n[No tool calling] Model response: {message.get('content')}\n")
        
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
                # TODO: testing
                print(f"\n[No tool calling] Model response: {content}\n")
                
                return content, None
            
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
        
    
    def call(self, api_name, input_params):
        """This is for calling 3rd party api directly without model"""
        
        # TODO
        
        raise NotImplementedError
    
    

