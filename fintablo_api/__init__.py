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

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "Fintablo",
    "FinTabloException",
    "AuthenticationException",
    "NotFoundException", 
    "ValidationException",
    "RateLimitException",
    "ServerException",
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
]