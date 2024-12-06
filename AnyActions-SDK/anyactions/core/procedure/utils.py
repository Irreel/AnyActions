import json
import inspect
from typing import List, Dict
from pathlib import Path
from anyactions.core.abstract import *

# from .register_api_tmp import *
# from .db_tmp import db, db_index, tool_name_to_index # db_tmp is to stimulate the real database


def create_inter_api_key(legal_api_name, api_dir_path, user, api_key_flg=1):
    """_summary_
    inter_api_key: refers to the 3rd party API key (We call it locally for now, might use it for future server to call them)
    
    Args:
        legal_api_name (_type_): A legal api name is formatted as [PROVIDER NAME]_[ACTION NAME] in upperletters
        api_dir_path: [Temporary] Keep the api key in local file
        user: For now, just a placeholder for user information
    Results:
        True, inter_api_key: create the api key successful
        True, '': the api key is optional and user did not provide one
        True, None: this api does not need api
        False, None: the request failed
    """
    try:
        provider_name, action_name = legal_api_name.split("_", maxsplit=1)
    except:
        print("Illegal API name. Please formatted as '[PROVIDER NAME]_[ACTION NAME]' in string")
    
    try:
        
        assert db[provider_name][action_name]["api_key_flg"] != 0 # Optional, removed if it called remote server
        
        match db[provider_name][action_name]: # The action exists
            case _:
                
                # TODO: For now it is just a stub code asking user to enter it manually / pretend it retrieves from a remote server
                if api_key_flg == 2:
                    print(f"\nAPI key is optional for {legal_api_name}. More details: {db[provider_name][action_name]['documentation']}")
                    x = input("Please enter the API key if you want to use it: ")
                    if x:
                        inter_api_key = x
                    else:
                        inter_api_key = ''
                        
                elif legal_api_name == "GOOGLE_SEARCH":
                    inter_api_key = register_api_tmp[legal_api_name]
                    
                with open(api_file_path, 'w') as f:
                    f.write(f"{legal_api_name}_KEY = '{inter_api_key}'\n")
                if len(inter_api_key) > 0:
                    print(f"Created a new API key for {legal_api_name} and saved into {api_dir_path}")
                else:
                    print(f"Created an empty API key for {legal_api_name} and saved into {api_dir_path}")
                
                return True, inter_api_key
            
            
            # TODO: Register a API key for developers? [HasBeenDiscussed]
            
            # TODO: There might be some APIs need to install their own libary mandatory. Maybe we can download those library in user local folder automatically?
                # Run terminal command to install their library
                # try:
                #     import subprocess
                #     subprocess.check_call(["pip", "install", "atlassian-python-api"])
                #     print("Successfully installed JIRA library")
                #     inter_api_key = input("Please enter your JIRA API token: ")
                #     return True, inter_api_key
                # except subprocess.CalledProcessError as e:
                #     print(f"Failed to install JIRA library: {e}")
                #     return False, None
                
            
        
    except Exception as e:
        print(e)
        return False, None
  
    
@deprecated
def definition(tool_list: List) -> List[dict]:
        """_summary_
        Args:
            tool_list: a list of tools to define. Each entry can be:
                - A string representing a pre-defined tool name
                - A dictionary containing a custom tool definition
                - A callable function (not yet implemented)

        This method processes the provided tool list and returns a list of tool definitions.
        For predefined tools (strings), it looks up the definition in the db_index.
        For custom tools (dictionaries), it adds them directly to the list.
        For callable functions, it's going to generate the definition based on the code.

        Raises:
            NotImplementedError: _description_

        Returns:
            List[dict]: _description_
        """

        if not isinstance(tool_list, list): tool_list = [tool_list]
        
        tool_definition_list = []
        for entry in tool_list:
            match entry:
                case str():
                    # If it is a tool name
                    legal_api_name = tool_name_to_index.get(entry, None) # tool_name_to_index is a stub code to stimulate the real database
                    if legal_api_name:
                        # RANDOM IDEA: Add a local mapping between tool name and legal api name?
                        provider_name = legal_api_name.split("_")[0]
                        action_name = legal_api_name.split("_", 1)[1]
                        tool_definition_list.append(db[provider_name][action_name]['ai_tool_desc'])
                        
                    else:
                        print(f"{entry} is not found in actions library")
                        tool_definition_list.append(entry)
                case dict():
                    tool_definition_list.append(entry)
                case callable():
                    # TODO
                    function_body = inspect.getsource(entry) 
                    # function_body = entry.__code__.co_code.decode()
                    print("An experimental function: get tool description from its code body (also generated by LLM?)")
                    print(function_body)
                    
                    tool_definition_list.append(function_to_json(entry))
                    
                case _:
                    raise ValueError("Unsupported tool type")
        
        return tool_definition_list
    

def check_dependencies(tool_list: List):
    """
    Check if the tool_list has all the dependencies
    """
    # TODO: request to the server?