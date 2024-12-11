import os
import json
import requests
from getpass import getpass
from dotenv import load_dotenv
from typing import List, Dict, Union, Optional

from anyactions.common import *
from anyactions.core.decorators import *
from anyactions.common.procedure.local import *
from anyactions.core.retrieve import Retriever
from anyactions.core.client import Client, RequestStatus

from anyactions.core.procedure.act import Actor

from anyactions.common.constants import LOCAL_ENV_PATH

class ActionHub:
    """
    This is the main class for managing tools and API calls.
    """
    
    def __init__(self, env={}, model_provider="openai", api_dir_path=LOCAL_ENV_PATH, observer=False):
        """
        Initialize the ActionHub class which manages tool loading, API key handling, and tool execution.
        
        Args:
            env (dict, optional): Environment variables for LLM configuration and user machine settings. 
            model_provider (str, optional): The LLM provider. Only supports "openai" now.
            api_dir_path (str, optional): Path to the directory storing API configurations and tools.
            observer (bool, optional): If True, print debug information. Defaults to False.
                
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
            get_tool_list (function -> List[str]): Get list of locally available tool names
            api_dir_path (str): Path to API directory
            api_keys_path (str): Path to API keys directory
            api_config_path (str): Path to config file
        """
        self.env = env
        self.observer = observer
        self.resolved_endpoint = {} #TODO: might not be necessary if tool function is generated
        
        ## Setup client
        load_dotenv()
        self.base_url = os.environ["AWS_GATEWAY_BASE_URL"]
        self.user = {
            "api_key": os.environ["AWS_GATEWAY_API_KEY"],
        }
        self.client = Client(self.base_url, self.user["api_key"])
        self.retriever = Retriever(self.client, self.observer)
        
        ## Local tool loading
        if os.path.exists(api_dir_path):
            pass
        else:
            create_local_tools_dir(api_dir_path)
        
        ## API Key Initialization
        self.api_dir_path = api_dir_path
        self.api_keys_path = os.path.join(api_dir_path, '.api_keys')
        self.api_config_path = os.path.join(api_dir_path, '.config')
        
        
    def get_local_tool_list(self):
        # This local tool list includes the tools that have been stored in the local file, notice this does not mean their api keys always work
        return get_all_local_tool_names(self.api_dir_path, self.observer)
        
    def tools(self, tool_list: List[str | dict]) -> List[dict]:
        """
        Initialize a set of tool definitions available to LLM
        It loads existing local tools and use retriever to set up new tools
        If the entry in tool_list is a dictionary, it is treated as the tool definition directly
        
        Args:
            tool_list (List[str | dict]): List of tool names or tool definitions

        Raises:
            Exception: tool definition parsing failed
            ValueError: tool definition is not in the correct format

        Returns:
            List[dict]: tool definition list
        """
        
        definition_list = []
        local_tool_list = self.get_local_tool_list()
        
        for i in tool_list: 
            if isinstance(i, str):
                # Load tools from local
                if i in local_tool_list:
                    check_local_tool_legit(self.api_dir_path, i, self.observer)
                    try:
                        definition_list.append(get_local_tool_definition(self.api_dir_path, i))
                    except Exception as e:
                        raise Exception(f"{i} Parse tool definition failed. Please check if {self.api_dir_path}{i}.py is valid: {e}")
                else:
                    # If not existed in local env, setup new tools
                    parsed_tool_def = self._setup_tool(i)
                    definition_list.append(parsed_tool_def)

            elif isinstance(i, dict):
                # The entry is a dictionary, add as the tool definition directly
                try:
                    # Format check
                    tool_def = ToolDefinition(**i)
                except Exception as e:
                    print(f"Invalid OpenAI tool definition format: {e}")
                    user_input = input("Still added to the tool definition list?(y/n)")
                    if user_input.lower() == "y":
                        definition_list.append(i)
                    else:
                        raise ValueError("Invalid tool definition format")

            else:
                raise ValueError("Tool list should be a list of strings or dictionaries")
        
        return definition_list
        
    def _setup_tool(self, tool_name) -> dict:
        """Set up a new tool by retrieving its definition and handling API key configuration.

        This internal method retrieves the tool definition from the server, writes it to the local
        environment, and handles API key setup if required.

        Args:
            tool_name (str): The name of the tool to set up

        Raises:
            Exception: If tool retrieval from the server fails
            Exception: If writing the tool to local environment fails
            Exception: If API key setup is required but not provided

        Returns:
            dict: tool definition dictionary subject to OpenAI tool calling schema
        """
        response = self.retriever(tool_name)
        
        try:
            gen_flg, instruction, tool_def, func_body = response
        except Exception as e:
            raise Exception(f"Failed to retrieve {tool_name} tool: {e}")
        
        try:
            write_local_tool(self.api_dir_path, tool_def, func_body)
            
            auth_flg = check_local_tool_auth_method(self.api_dir_path, tool_name)
            
            if auth_flg:
                # If api key is required or optional
                if not check_local_api_key_exists(self.api_dir_path, tool_name):
                    print(f"You can set up the API key here: {instruction}\n")
                    api_key = getpass("Paste your API key here:")
                    if api_key:
                        with open(os.path.join(self.api_dir_path, '.api_keys', f"{tool_name.upper()}_KEY"), 'w+') as f:
                            f.write(f"{api_key}")
                    else:
                        if auth_flg == 2:
                            print(f"API key is optional for {tool_name}. Continue without authentication.")
                        elif auth_flg == 1:
                            raise Exception("API key is required")
                else:
                    # If the api key already exists, do nothing
                    if self.observer:
                        print(f"{tool_name} API key already found")
                    pass
            
            if self.observer:
                print(f"{tool_name}.py added")            
            return tool_def
        
        except Exception as e:
            raise Exception(f"Failed to set up {tool_name} tool in local environment: {e}")
      
    @deprecated
    def verification(self, api_name):
        """_summary_
        @deprecated
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
                    if line.strip().startswith(f"{legal_api_name}_KEY"):
                        api_key_found = True
                        # Extract the inter_api_key from the line
                        inter_api_key = line.strip().split('=')[1].strip().strip("'")
                        break
                    
        if not api_key_found:
            status = False
            if api_key_flg == 1:
                # If local API key is not found
                # status, inter_api_key = create_inter_api_key(legal_api_name, self.api_file_path, self.user, api_key_flg=api_key_flg) 
                # TODO 
                raise NotImplementedError
            elif api_key_flg == 2:
                # If api key is optional, still create a null string
                print(f"API key is optional for {legal_api_name}. Do not use key temporarily.")
                inter_api_key = ''
                status = True   
    
            if status:
                with open(self.api_file_path, 'w') as f:
                    f.write(f"{legal_api_name}_KEY = '{inter_api_key}'\n")
            else:
                raise ValueError(f"Failed to create {legal_api_name} key")  
        
        return True, provider_name, action_name, inter_api_key

    @deprecated
    def _act_mock(self, api_name, input_params, endpoint_cache=True):

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

    def act(self, response_object):
        """Execute the action based on response object and return the raw response"""
        response = Actor(self.api_dir_path, self.client, self.observer)(response_object)
        return response

        
    def call(self, action_name: str, input_params: dict):
        """call tool functions directly without model"""
        # TODO
        raise NotImplementedError
    
    

