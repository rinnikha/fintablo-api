"""
Fintablo API Python Client

A Python client library for interacting with the Fintablo API.
"""

from .client import Fintablo
from .exceptions import (
    FinTabloException,
    AuthenticationException,
    NotFoundException,
    ValidationException,
    RateLimitException,
    ServerException,
    TimeoutException,
    ConnectionException,
    BadRequestException,
    ForbiddenException,
    ModelParsingException,
    EmptyResponseException,
)
from .models import (
    Category,
    Moneybag,
    Partner,
    Direction,
    Transaction,
    Deal,
    Employee,
    Goods,
    Job,
    Obligation,
    GroupEnum,
)
from .logging_utils import setup_logging, get_logger as _get_logger

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

get_logger = _get_logger

__all__ = [
    "Fintablo",
    # Exceptions
    "FinTabloException",
    "AuthenticationException",
    "NotFoundException",
    "ValidationException",
    "RateLimitException",
    "ServerException",
    "TimeoutException",
    "ConnectionException",
    "BadRequestException",
    "ForbiddenException",
    "ModelParsingException",
    "EmptyResponseException",
    # Models
    "Category",
    "Moneybag",
    "Partner",
    "Direction",
    "Transaction",
    "Deal",
    "Employee",
    "Goods",
    "Job",
    "Obligation",
    "GroupEnum",
    # Utilities
    "setup_logging",
    "get_logger",
]
