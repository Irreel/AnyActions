import os
import json
import requests
from getpass import getpass
from dotenv import load_dotenv
from typing import List, Dict, Union, Optional, Callable

from anyactions.common import *
from anyactions.core.decorators import *
from anyactions.common.local import *
from anyactions.core import Retriever, Actor
from anyactions.core.client import Client, RequestStatus

from anyactions.common.constants import LOCAL_ENV_PATH, LOCAL_AUTH_PATH, CONFIG_PATH

class ActionHub:
    """
    This is the main class for managing tools and API calls.
    """
    
    def __init__(self, env={}, model_provider="openai", api_dir_path=LOCAL_ENV_PATH, auth_dir_path=LOCAL_AUTH_PATH, config_path=CONFIG_PATH, observer=True):
        """
        Initialize the ActionHub class which manages tool loading, API key handling, and tool execution.
        
        Args:
            env (dict, optional): Environment variables for LLM configuration and user machine settings. 
            model_provider (str, optional): The LLM provider. Only supports "openai" now.
            api_dir_path (str, optional): Path to the directory storing tool functions.
            auth_dir_path (str, optional): Path to the directory storing API keys.
            config_path (str, optional): Path to the configuration file.
            observer (bool, optional): If True, print debug information. Defaults to True.
                
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
        self.client = Client(self.base_url, self.user["api_key"], self.observer)
        self.retriever = Retriever(self.client, self.observer)
        
        ## Local tool loading
        if os.path.exists(api_dir_path):
            pass
        else:
            create_local_tools_dir(api_dir_path, auth_dir_path)
        
        ## API Key Initialization
        self.api_dir_path = api_dir_path
        # self.api_keys_path = os.path.join(api_dir_path, '.api_keys')
        self.auth_dir_path = auth_dir_path
        self.api_config_path = config_path
        
        
    def get_local_action_list(self):
        # This local tool list includes the tools that have been stored in the local file, notice this does not mean their api keys always work
        return get_all_local_tool_names(self.api_dir_path, self.observer)
        
    def get_all_config(self):
        with open(self.api_config_path, 'r') as f:
            return json.load(f)
        
    def update_tool_config(self, action_name: str, config: dict):
        current_config = self.get_all_config()
        
        current_config[action_name] = config
        with open(self.api_config_path, 'w') as f:
            json.dump(current_config, f)
        if self.observer:
            print(f"Updated {action_name} config: {config.keys()}")
    
    def set_key(self, action_name: str, api_key: str):
        """Set up authentication (API key) for a tool by adding an API key to the local environment"""
        try:
            write_local_key(self.auth_dir_path, action_name, api_key)
            print(f"Added authentication for {action_name} successfully")
            return True
        except Exception as e:
            print(f"Failed to set up authentication for {action_name}: {e}")
            return False
        
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
        local_tool_list = self.get_local_action_list()
        
        for i in tool_list: 
            if isinstance(i, str):
                # Load tools from local
                if i in local_tool_list:
                    check_local_tool_legit(self.api_dir_path, self.auth_dir_path, i, self.observer)
                    try:
                        definition_list.append(get_local_tool_definition(self.api_dir_path, self.auth_dir_path, i))
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
    
    def tools_func(self, tool_list: List[str | Callable]) -> List[Callable]:
        """
        Initialize a set of tool definitions available to LLM
        It loads existing local tools and use retriever to set up new tools
        If the entry in tool_list is a callable, it is treated as the tool definition directly
        
        Args:
            tool_list (List[str | Callable]): List of tool names or tool definitions

        Raises:
            Exception: tool definition parsing failed
            ValueError: tool definition is not in the correct format

        Returns:
            List[dict]: tool definition list
        """
        
        callable_list = []
        local_tool_list = self.get_local_action_list()
        
        for i in tool_list: 
            if isinstance(i, str):
                # Load tools from local
                if i in local_tool_list:
                    try:
                        check_local_tool_legit(self.api_dir_path, self.auth_dir_path, i, self.observer)
                    except AssertionError as e:
                        print(e)
                    try:
                        callable_list.append(get_tool_callable(file_path=os.path.join(self.api_dir_path, f"{i}.py"), action_name=i))
                    except Exception as e:
                        raise Exception(f"{i} Parse tool definition failed. Please check if {self.api_dir_path}{i}.py is valid: {e}")
                else:
                    # If not existed in local env, setup new tools
                    parsed_tool_def = self._setup_tool(i)
                    callable_list.append(get_tool_callable(file_path=os.path.join(self.api_dir_path, f"{i}.py"), action_name=i))

            elif isinstance(i, Callable):
                # The entry is a Callable, add as the tool directly
                    callable_list.append(i)

            else:
                raise ValueError("Tool list should be a list of strings or callables")
        
        return callable_list
        
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
            if self.observer:
                print(f"Retrieved tool function: {tool_name}")
        except Exception as e:
            raise Exception(f"Failed to retrieve {tool_name} tool: {e}")
        
        try:
            write_local_tool(self.api_dir_path, tool_def, func_body)
            
            auth_flg = check_local_tool_auth_method(self.api_dir_path, tool_name)
            
            if auth_flg:
                # If api key is required or optional
                if not check_local_api_key_exists(self.auth_dir_path, tool_name):
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
  
  
    def act(self, response_object):
        """Execute the action based on response object and return the raw response"""
        response = Actor(self.api_dir_path, self.auth_dir_path, self.client, self.observer)(response_object)
        return response

        
    def call(self, action_name: str, input_params: dict, is_auth: bool = False):
        """Call tool functions directly without model
        Args:
            action_name (str): The name of the action to call. Should be the function name and file name in the tool directory.
            input_params (dict): The input parameters for the function calling
            is_auth (bool): Indicate if the action requires AnyActions to handle authentication
        """
        params = input_params.copy()
        if is_auth:
            auth_flg = check_local_tool_auth_method(self.api_dir_path, action_name)
              
            if auth_flg:
                # If api key is required or optional
                if not check_local_api_key_exists(self.auth_dir_path, action_name):
                    print(f"You can set up the API key for {action_name} here: {instruction}\n")
                    api_key = getpass("Paste your API key here:")
                    if api_key:
                        with open(os.path.join(self.api_dir_path, '.api_keys', f"{action_name.upper()}_KEY"), 'w+') as f:
                            f.write(f"{api_key}")
                        params['api_key'] = api_key
                    else:
                        if auth_flg == 2:
                            print(f"API key is optional for {action_name}. Continue without authentication.")
                        elif auth_flg == 1:
                            print("API key is required but missing. May cause failure in the following calling.")
                else:
                    # If the api key already exists, load it
                    if self.observer:
                        print(f"{action_name} API key already found")
                    params['api_key'] = get_local_api_key(self.auth_dir_path, action_name)
            
        func = get_tool_callable(action_name, os.path.join(self.api_dir_path, f"{action_name}.py"))
        return func(**params)
                
                
    def safe_call(self, action_name: str, input_params: dict):
        """Call tool functions directly without model, and handle API key by AnyActions.
        Args:
            action_name (str): The name of the action to call. Should be the function name and file name in the tool directory.
            input_params (dict): The input parameters for the function calling
        """
        return self.call(action_name, input_params, is_auth = True)
    
    


