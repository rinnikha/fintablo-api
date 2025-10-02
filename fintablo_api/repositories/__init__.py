"""
Repository classes for different Fintablo API endpoints.
"""

from .categories import CategoryRepository
from .moneybags import MoneybagRepository
from .transactions import TransactionRepository
from .partners import PartnerRepository
from .deals import DealRepository

__all__ = [
    "CategoryRepository",
    "MoneybagRepository",
    "TransactionRepository",
    "PartnerRepository",
    "DealRepository",
]