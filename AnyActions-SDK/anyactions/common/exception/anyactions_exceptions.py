class AnyActionsException(Exception):
    def __init__(self, message, cause: Exception = None):
        self.message = message
        self.cause = cause

    def __str__(self):
        return self.message.__str__()
    
    def __repr__(self):
        return self.message.__repr__()
    
class LocalToolException(AnyActionsException):
    def __init__(self, message, cause: Exception = None):
        super().__init__(message, cause)
    
class AWSInternalException(AnyActionsException):
    def __init__(self, message, cause: Exception = None):
        super().__init__(message, cause)


class AWSGatewayException(AnyActionsException):
    def __init__(self, message, cause: Exception = None):
        super().__init__(message, cause)