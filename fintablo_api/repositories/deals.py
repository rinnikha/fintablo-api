"""Deal repository for FinTablo API."""

from typing import Dict, Any, List

from ..base import BaseRepository
from ..http_client import HttpClient
from ..models import Deal


class DealRepository(BaseRepository[Deal]):
    """Repository for managing deals (сделки)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/deal", Deal)

    def get_by_partner(self, partner_id: int) -> List[Deal]:
        """Get deals by partner."""
        return self._list({"partnerId": partner_id})

    def get_by_status(self, status_id: int) -> List[Deal]:
        """Get deals by status."""
        return self._list({"statusId": status_id})

    def get_by_direction(self, direction_id: int) -> List[Deal]:
        """Get deals by direction."""
        return self._list({"directionId": direction_id})

    def get_by_responsible(self, responsible_id: int) -> List[Deal]:
        """Get deals by responsible person."""
        return self._list({"responsibleId": responsible_id})

    def add_stage(self, deal_id: int, stage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a stage to a deal."""
        return self.http_client.post(f"/{self.endpoint}/{deal_id}/add-stage", data=stage_data)
