"""Category repository for FinTablo API."""

from typing import List

from ..base import BaseRepository
from ..http_client import HttpClient
from ..models import Category


class CategoryRepository(BaseRepository[Category]):
    """Repository for managing categories (статьи)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/category", Category)

    def get_by_parent(self, parent_id: int) -> List[Category]:
        """Get categories by parent ID."""
        return self._list({"parentId": parent_id})

    def get_by_group(self, group: str) -> List[Category]:
        """
        Get categories by group.

        Args:
            group: One of 'income', 'outcome', 'transfer'
        """
        return self._list({"group": group})

    def get_by_type(self, category_type: str) -> List[Category]:
        """
        Get categories by type.

        Args:
            category_type: One of 'operating', 'financial', 'investment'
        """
        return self._list({"type": category_type})

    def get_by_pnl_type(self, pnl_type: str) -> List[Category]:
        """Get categories by P&L type."""
        return self._list({"pnlType": pnl_type})

    def get_income_categories(self) -> List[Category]:
        """Get all income categories."""
        return self.get_by_group("income")

    def get_outcome_categories(self) -> List[Category]:
        """Get all outcome categories."""
        return self.get_by_group("outcome")

    def get_transfer_categories(self) -> List[Category]:
        """Get all transfer categories."""
        return self.get_by_group("transfer")
