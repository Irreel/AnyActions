import os
import json
import inspect
from typing import Any, Optional, Union, Tuple, Callable

from anyactions.core.client import Client
from anyactions.core.decorators import action, generated_action

from anyactions.common import *
from anyactions.common.constants import *
from anyactions.common.protocol.protocols import ACTION_SUCCESS, ACTION_FAILURE
from anyactions.common.procedure.local import get_local_api_key, check_tool_decorator, get_tool_callable, validate_local_tool

class Actor:
    def __init__(self, api_dir_path: str, client = Client, observer=False):
        self.api_dir_path = api_dir_path
        self.client = client
        self.observer = observer
    
    def __call__(self, response_object):
        """Process and execute tool/function calls based on raw LLM response objects.
        
        This method intended to handle different types of response objects from various LLM providers
        (like OpenAI and Anthropic) and executes the requested tool/function calls.
        # TODO: Only support OpenAI for now
        
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
        
        # TODO: Finish the following implementation for multiple tool calls
        # if isinstance(response_object, list):
        #     if len(response_object) == 1:
        #         response_object = response_object[0]
        #     else:
        #         # This is useful for LLM responses which include a tool usage request with other text response 
        #         for entry in response_object:
        #             # Assume there is only one tool usage request in model responses
        #             try:
        #                 response, output_schema = self.act(entry)
        #                 # break once it found the tool usage request
        #                 break
        #             except:
        #                 pass
        #         return response, output_schema
        # else:
        
        # TODO: find a better way to identify the object without installing 3rd party package. 
        # (Solution 1: some packages re-write these object definition in their library, like langchain, litellm etc.)
        
        response = dict(response_object)
            
        # Check if it is ChatCompletion object in openai
        if ('choices' in response and
            isinstance(response['choices'], list) and
            len(response['choices']) > 0 and
            'message' in dict(response['choices'][0])):
            
            # Find the message with tool calls
            for choice in response['choices']:
                message = dict(dict(choice)['message'])
                if message.get('tool_calls', None) is not None:
                    for tool_call in message['tool_calls']:
                        tool_call_dict = dict(tool_call)
                        if tool_call_dict.get('type') == 'function':
                            function_name = dict(tool_call_dict['function'])['name']
                            function_args = json.loads(dict(tool_call_dict['function'])['arguments'])
                            if self.observer:
                                print(f"Function to call: {function_name}")
                                print(f"Arguments: {function_args}")
                            break
        
        # if it is ChatCompletionMessage object from OpenAI
        # ...
        
        # if it is ChatCompletionMessageToolCall object from OpenAI
        # ...
        
        # # Check if it is a ToolUseBlock-like object in claude 
        # elif (isinstance(response_object, dict) and
        #     'name' in response_object and
        #     'input' in response_object):
        #         function_name = response_object['name']
        #         function_args = response_object['input']
      
        # # if it is <class 'anthropic.types.message.Message'> in claude
        # elif (isinstance(response_object, dict) and
        #     'content' in response_object and
        #     'stop_reason' in response_object):
            
        #     content = response_object['content']
            
        #     if response_object['stop_reason'] == 'tool_use':
        #         for item in content:
        #             # TODO: find a better way to identify these object
        #             item = dict(item)
        #             if item['type'] == 'text':
        #                 pass
        #             elif item['type'] == 'tool_use':
        #                 function_name = item['name']
        #                 function_args = item['input']
                        
        #                 print(f"  Tool name: {item['name']}")
        #                 print(f"  Tool input: {json.dumps(item['input'], indent=2)}")
        #     else:
        #         # TODO: testing
        #         print(f"\n[No tool calling] Model response: {content}\n")
                
        #         return content, None
            
        else:
            raise Exception("Unsupported response object type")
        
        if 'function_name' not in locals():
            # If there are no tool calls, just print the content
            if self.observer:
                print("\nNo tool calling object found in the model response\n")
            return response_object
        
        response = self._act_local(function_name, function_args)
        
        return response
    
    def call(self, action_name, input_params: dict, api_key=None):
        """Call a tool function from a local Python file manually.
        """
        raise NotImplementedError
    
    def _act_local(self, action_name, input_params: dict):
        """Execute a tool function from a local Python file.
        
        Args:
            action_name (str): Name of the tool/function to execute
            input_params (dict): Parameters to pass to the function
        
        Returns:
            tuple: response
        
        Raises:
            ImportError: If the tool module cannot be imported
            AttributeError: If the tool function cannot be found in the module
            Exception: For any other errors during execution
        """
        try:
            # Construct the file path
            module_path = os.path.join(self.api_dir_path, f"{action_name}.py")
            assert os.path.exists(module_path), LocalToolException(f"Tool {action_name} not found in {module_path}. Please check if the tool function file exists.")
            
            # Load the module
            tool_function = get_tool_callable(action_name, module_path)
            
            # Get the function signature parameters
            params = inspect.signature(tool_function).parameters
            
            # Handle api_key parameter if the function requires it
            if 'api_key' in params:
                if 'api_key' not in input_params:
                    api_key = get_local_api_key(self.api_dir_path, action_name)
                    input_params['api_key'] = api_key
            
            if check_tool_decorator(tool_function, 'generated_action', self.observer):
                # Get the output schema if it exists in the module
                # output_schema = getattr(module, 'output_schema', None)
                
                # TODO: use MCP
                response, status = tool_function(**input_params)
                if status == ACTION_SUCCESS:
                    self.callback(action_name, tool_function, self.observer)
                    validate_local_tool(self.api_dir_path, action_name, self.observer)
                    return response
                elif status == ACTION_FAILURE:
                    raise Exception(f"Error executing tool {module_path}: {response}")
                
            else:
                # TODO: use MCP
                return tool_function(**input_params)
            
        except ImportError as e:
            raise ImportError(f"Failed to import tool module {action_name}: {e}")
        except AttributeError as e:
            raise AttributeError(f"Tool function {action_name} not found in module: {e}")
        except Exception as e:
            raise Exception(f"Error executing tool {action_name}: {e}")

    def callback(self, action_name: str, tool_function: Callable, observer=False):
        response = self.client.post(path=CALLBACK_EP, data=self.upload_request(action_name, tool_function))
        if observer:
            print(f"Callback to {CALLBACK_EP} with action_name: {action_name}")
        return response
    
    def upload_request(self, action_name: str, tool_function: Callable) -> dict:
        builder = CallbackApiRequestBuilder()
        builder.set_action(action_name)
        # builder.set_tool_function(tool_function)
        return builder.get()

    
