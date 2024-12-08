import inspect
import warnings
import functools

from anyactions.common.protocol.protocols import ACTION_SUCCESS, ACTION_FAILURE

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def generated_action(func):
    """This is a decorator which can be used to mark functions
    as an action. It will result in a callback when the function is used."""

    @functools.wraps(func)
    def callback(*args, **kwargs):
        try:
            action_result = func(*args, **kwargs)
            return action_result, ACTION_SUCCESS
        except Exception as e:
            return e, ACTION_FAILURE
    
    callback.__name__ = "generated_action"
    
    return callback


def action(func):
    
    @functools.wraps(func)
    def callback(*args, **kwargs):
        # PENDING: check if the function is already verified??
        
        # # Get function parameters
        # params = inspect.signature(func).parameters
        
        # api_key_index = None
        # for i, (param_name, _) in enumerate(params.items()):
        #     if param_name == 'api_key':
        #         api_key_index = i
        #         break
        
        # # Handle api_key parameter if the function requires it
        # if api_key_index is not None and 'api_key' not in kwargs and api_key_index < len(args):
        #     # Assuming first arg is 'self' for class methods
        #     if args and hasattr(args[0], 'api_dir_path'):
        #         self = args[0]
        #         action_name = func.__name__
        #         api_key = get_local_api_key(self.api_dir_path, action_name)
        #         kwargs['api_key'] = api_key

        # try:
        #     response = func(*args, **kwargs)
        #     return response
        # except Exception as e:
        #     raise Exception(f"Error executing action '{func.__name__}': {e}")
        
        return func(*args, **kwargs)
    
    callback.__name__ = "action"
    
    return callback
