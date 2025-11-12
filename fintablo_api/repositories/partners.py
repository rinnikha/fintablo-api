"""Partner repository for FinTablo API."""

from typing import List

from ..base import BaseRepository
from ..http_client import HttpClient
from ..models import Partner


class PartnerRepository(BaseRepository[Partner]):
    """Repository for managing partners (контрагенты)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/partner", Partner)

    def search_by_name(self, name: str) -> List[Partner]:
        """Search partners by name."""
        return self._list({"name": name})

    def get_by_inn(self, inn: str) -> List[Partner]:
        """Get partners by INN."""
        return self._list({"inn": inn})

    def get_by_group(self, group_id: int) -> List[Partner]:
        """Get partners by group ID."""
        return self._list({"groupId": group_id})

    def search_by_comment(self, comment: str) -> List[Partner]:
        """Search partners by comment."""
        return self._list({"comment": comment})
