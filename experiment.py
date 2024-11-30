from abc import ABC, abstractmethod
from functools import wraps

import inspect


# Abstract decorator class
class FunctionDecorator(ABC):
    def __init__(self, func):
        self.func = func
        self.has_run_successfully = False  # To track the first successful run

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)
            if not self.has_run_successfully:
                self.has_run_successfully = True
                self.on_first_success()
            return result
        except Exception as e:
            print(f"Error: {e}")
            raise  # Re-raise the exception if there's an error

    @abstractmethod
    def on_first_success(self):
        pass

# Concrete decorator class
class WooDecorator(FunctionDecorator):
    def on_first_success(self):
        body = inspect.getsource(self.func)
        print(f"Function body: {body}")
        print("Callback executed on first successful run.")

# Decorate a function
@WooDecorator
def Woo():
    print("Executing Woo function.")
    # Perform any operations here
    # If there's an error, you could raise an exception

# Example usage
try:
    Woo()  # First call, should trigger the callback
    Woo()  # Subsequent calls, no callback
except Exception as e:
    print("Exception handled:", e)