"""
Exception classes for the Fintablo API client.
"""


class FinTabloException(Exception):
    """Base exception class for all Fintablo API errors."""
    
    def __init__(self, message, response=None, status_code=None):
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code = status_code
    
    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationException(FinTabloException):
    """Raised when authentication fails or API key is invalid."""
    pass


class NotFoundException(FinTabloException):
    """Raised when a requested resource is not found."""
    pass


class ValidationException(FinTabloException):
    """Raised when request validation fails."""
    
    def __init__(self, message, response=None, status_code=None, errors=None):
        super().__init__(message, response, status_code)
        self.errors = errors or []


class RateLimitException(FinTabloException):
    """Raised when API rate limits are exceeded."""
    
    def __init__(self, message, response=None, status_code=None, retry_after=None):
        super().__init__(message, response, status_code)
        self.retry_after = retry_after


class ServerException(FinTabloException):
    """Raised when the server returns a 5xx error."""
    pass


class TimeoutException(FinTabloException):
    """Raised when a request times out."""
    pass


class ConnectionException(FinTabloException):
    """Raised when there are connection issues."""
    pass