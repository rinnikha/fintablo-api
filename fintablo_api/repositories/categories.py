"""
Category repository for FinTablo API.
"""

from typing import Dict, Any, List, Optional
from ..base import BaseRepository
from ..models import Category
from ..http_client import HttpClient


class CategoryRepository(BaseRepository[Category]):
    """Repository for managing categories (статьи)."""
    
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/category", Category)
    
    def get_by_parent(self, parent_id: int) -> List[Category]:
        """Get categories by parent ID."""
        params = {"parentId": parent_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_group(self, group: str) -> List[Category]:
        """
        Get categories by group.
        
        Args:
            group: One of 'income', 'outcome', 'transfer'
        """
        params = {"group": group}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_type(self, category_type: str) -> List[Category]:
        """
        Get categories by type.
        
        Args:
            category_type: One of 'operating', 'financial', 'investment'
        """
        params = {"type": category_type}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_pnl_type(self, pnl_type: str) -> List[Category]:
        """Get categories by P&L type."""
        params = {"pnlType": pnl_type}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_income_categories(self) -> List[Category]:
        """Get all income categories."""
        return self.get_by_group("income")
    
    def get_outcome_categories(self) -> List[Category]:
        """Get all outcome categories."""
        return self.get_by_group("outcome")
    
    def get_transfer_categories(self) -> List[Category]:
        """Get all transfer categories."""
        return self.get_by_group("transfer")
    
    def _create_models_from_response(self, data: Dict[str, Any]) -> List[Category]:
        """Create model instances from API response."""
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        else:
            items = data if isinstance(data, list) else [data]
        
        return [self._create_model(item) for item in items if item]