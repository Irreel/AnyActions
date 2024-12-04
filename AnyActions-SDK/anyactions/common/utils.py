import warnings
import functools

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
        
        # Step 1: Read local file to specify if the function is already verified
        # TODO: Implement this
        # Step 2: If verified, call the function directly
        if False:
            return func(*args, **kwargs)
        # Step 3: If not verified, call the function and upload the result to the server
        else:
            print("Mock function callback to our server")
            print(func.__code__[:10])
        
            return func(*args, **kwargs)
    
    return callback

def action(func):
    return func
