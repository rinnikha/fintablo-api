"""Transaction repository for FinTablo API."""

from typing import Dict, Any, List, Optional

from ..base import BaseRepository
from ..exceptions import NotFoundException
from ..http_client import HttpClient
from ..models import Transaction


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for managing transactions (операции ДДС)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/transaction", Transaction)

    def get_by_account(self, moneybag_id: int) -> List[Transaction]:
        """Get transactions for a specific account."""
        return self._list({"moneybagId": moneybag_id})

    def get_by_category(self, category_id: int) -> List[Transaction]:
        """Get transactions by category."""
        return self._list({"categoryId": category_id})

    def get_by_partner(self, partner_id: int) -> List[Transaction]:
        """Get transactions by partner."""
        return self._list({"partnerId": partner_id})

    def get_by_direction(self, direction_id: int) -> List[Transaction]:
        """Get transactions by direction."""
        return self._list({"directionId": direction_id})

    def get_by_deal(self, deal_id: int) -> List[Transaction]:
        """Get transactions by deal."""
        return self._list({"dealId": deal_id})

    def get_by_date_range(self, date_from: str, date_to: str) -> List[Transaction]:
        """
        Get transactions within a date range.

        Args:
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
        """
        return self._list({"dateFrom": date_from, "dateTo": date_to})

    def get_by_group(self, group: str) -> List[Transaction]:
        """
        Get transactions by group.

        Args:
            group: One of 'income', 'outcome', 'transfer'
        """
        return self._list({"group": group})

    def get_income_transactions(self) -> List[Transaction]:
        """Get all income transactions."""
        return self.get_by_group("income")

    def get_outcome_transactions(self) -> List[Transaction]:
        """Get all outcome transactions."""
        return self.get_by_group("outcome")

    def get_transfer_transactions(self) -> List[Transaction]:
        """Get all transfer transactions."""
        return self.get_by_group("transfer")

    def get_planned_transactions(self) -> List[Transaction]:
        """Get planned transactions."""
        return self._list({"isPlan": True})

    def get_actual_transactions(self) -> List[Transaction]:
        """Get actual (non-planned) transactions."""
        return self._list({"isPlan": False})

    def split_transaction(self, transaction_id: int, split_data: Dict[str, Any]) -> Dict[str, Any]:
        """Split a transaction into multiple parts."""
        return self.http_client.post(f"/{self.endpoint}/{transaction_id}/split", data=split_data)

    def unsplit_transaction(self, transaction_id: int) -> Dict[str, Any]:
        """Unsplit a transaction."""
        return self.http_client.post(f"/{self.endpoint}/{transaction_id}/unsplit")

    def merge_transactions(self, transaction_id1: int, transaction_id2: int) -> Dict[str, Any]:
        """Merge two transactions."""
        return self.http_client.post(f"/{self.endpoint}/{transaction_id1}/merge/{transaction_id2}")

    def convert_to_transfer(
        self, transaction_id: int, transfer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert transaction to transfer."""
        return self.http_client.post(
            f"/{self.endpoint}/{transaction_id}/to-transfer", data=transfer_data
        )

    def split_transfer(self, transaction_id: int, split_data: Dict[str, Any]) -> Dict[str, Any]:
        """Split transfer transaction."""
        return self.http_client.post(
            f"/{self.endpoint}/{transaction_id}/split-transfer", data=split_data
        )

    def confirm_transaction(self, transaction_id: int) -> Dict[str, Any]:
        """Confirm a transaction."""
        return self.http_client.post(f"/{self.endpoint}/{transaction_id}/confirm")
