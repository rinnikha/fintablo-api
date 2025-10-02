"""
Moneybag repository for FinTablo API.
"""

from typing import Dict, Any, List, Optional
from ..base import BaseRepository
from ..models import Moneybag
from ..http_client import HttpClient


class MoneybagRepository(BaseRepository[Moneybag]):
    """Repository for managing moneybags (accounts/счета)."""
    
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/moneybag", Moneybag)
    
    def get_by_type(self, account_type: str) -> List[Moneybag]:
        """
        Get accounts by type.
        
        Args:
            account_type: One of 'nal', 'bank', 'card', 'electron', 'acquiring'
        """
        params = {"type": account_type}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_currency(self, currency: str) -> List[Moneybag]:
        """Get accounts by currency."""
        params = {"currency": currency}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_group(self, group_id: int) -> List[Moneybag]:
        """Get accounts by group ID."""
        params = {"groupId": group_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_active_accounts(self) -> List[Moneybag]:
        """Get all non-archived accounts."""
        params = {"archived": False}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_archived_accounts(self) -> List[Moneybag]:
        """Get all archived accounts."""
        params = {"archived": True}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_cash_accounts(self) -> List[Moneybag]:
        """Get all cash accounts."""
        return self.get_by_type("nal")
    
    def get_bank_accounts(self) -> List[Moneybag]:
        """Get all bank accounts."""
        return self.get_by_type("bank")
    
    def get_card_accounts(self) -> List[Moneybag]:
        """Get all card accounts."""
        return self.get_by_type("card")
    
    def search_by_name(self, name: str) -> List[Moneybag]:
        """Search accounts by name."""
        params = {"name": name}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def _create_models_from_response(self, data: Dict[str, Any]) -> List[Moneybag]:
        """Create model instances from API response."""
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        else:
            items = data if isinstance(data, list) else [data]
        
        return [self._create_model(item) for item in items if item]