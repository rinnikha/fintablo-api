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


class ModelParsingException(FinTabloException):
    """Raised when there's an error parsing API response into a model."""

    def __init__(self, model_class, api_data, original_error):
        self.model_class = model_class
        self.api_data = api_data
        self.original_error = original_error

        model_name = model_class.__name__ if hasattr(model_class, "__name__") else str(model_class)
        api_keys = list(api_data.keys()) if isinstance(api_data, dict) else "non-dict data"
        expected_fields = (
            list(model_class.__annotations__.keys())
            if hasattr(model_class, "__annotations__")
            else "unknown"
        )

        message = (
            f"Failed to parse API response into {model_name} model.\n"
            f"Original error: {str(original_error)}\n"
            f"API data keys: {api_keys}\n"
            f"Expected model fields: {expected_fields}"
        )
        super().__init__(message)


class EmptyResponseException(FinTabloException):
    """Raised when API returns an empty response when data was expected."""

    def __init__(self, endpoint):
        self.endpoint = endpoint
        message = f"API returned empty response for endpoint: {endpoint}"
        super().__init__(message)


class BadRequestException(FinTabloException):
    """Raised when the request is malformed or invalid (400)."""
    pass


class ForbiddenException(FinTabloException):
    """Raised when access to resource is forbidden (403)."""
    pass