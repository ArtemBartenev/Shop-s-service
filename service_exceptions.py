"""
Base exceptions for shop service
"""
class ServiceBaseException(Exception):
    """Basic exception for errors raised by service working"""

    def __init__(self, message=None):
        if message is None:
            message = "Service is unavailable now"
        super().__init__(message)


class ServiceExecuteError(ServiceBaseException):
    """Raised when service has not registered operation(s)"""

    def __init__(self):
        super().__init__("Service has not registered operations")


class ServiceValidationError(ServiceBaseException):
    """Raised when service received invalid params"""

    def __init__(self, message):
        super().__init__(message)


class ServiceConnectionError(ServiceBaseException):
    """Raised when service has trouble(s) with connection"""

    def __init__(self):
        super().__init__("Service cannot connect to host")


class ServiceDataBaseError(ServiceBaseException):
    """Raised when service made bad request to database"""

    def __init__(self, message):
        super().__init__(message)
