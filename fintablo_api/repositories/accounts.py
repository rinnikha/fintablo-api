"""
Account repository and model for Fintablo API.
"""

from typing import Dict, Any, List, Optional
from ..base import BaseRepository, BaseModel
from ..http_client import HttpClient


class Account(BaseModel):
    """Account model representing a financial account."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        
        # Common account fields (to be adjusted based on actual API)
        self.id: Optional[str] = data.get('id')
        self.name: Optional[str] = data.get('name')
        self.type: Optional[str] = data.get('type')
        self.balance: Optional[float] = data.get('balance')
        self.currency: Optional[str] = data.get('currency')
        self.status: Optional[str] = data.get('status')
        self.created_at: Optional[str] = data.get('created_at')
        self.updated_at: Optional[str] = data.get('updated_at')


class AccountRepository(BaseRepository[Account]):
    """Repository for managing accounts."""
    
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "accounts", Account)
    
    def get_by_type(self, account_type: str) -> List[Account]:
        """Get accounts by type."""
        return self.query().filter(type=account_type).execute()
    
    def get_active_accounts(self) -> List[Account]:
        """Get all active accounts."""
        return self.query().filter(status="active").execute()
    
    def get_balance_summary(self) -> Dict[str, Any]:
        """Get balance summary for all accounts."""
        # This would be a custom endpoint specific to Fintablo
        data = self.http_client.get(f"/{self.endpoint}/balance-summary")
        return data
    
    def search_by_name(self, name: str) -> List[Account]:
        """Search accounts by name."""
        return self.query().filter(name__icontains=name).execute()