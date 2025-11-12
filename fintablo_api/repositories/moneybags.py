"""Moneybag repository for FinTablo API."""

from typing import List

from ..base import BaseRepository
from ..http_client import HttpClient
from ..models import Moneybag


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
        return self._list({"type": account_type})

    def get_by_currency(self, currency: str) -> List[Moneybag]:
        """Get accounts by currency."""
        return self._list({"currency": currency})

    def get_by_group(self, group_id: int) -> List[Moneybag]:
        """Get accounts by group ID."""
        return self._list({"groupId": group_id})

    def get_active_accounts(self) -> List[Moneybag]:
        """Get all non-archived accounts."""
        return self._list({"archived": False})

    def get_archived_accounts(self) -> List[Moneybag]:
        """Get all archived accounts."""
        return self._list({"archived": True})

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
        return self._list({"name": name})
