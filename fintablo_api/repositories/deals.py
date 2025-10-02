"""
Deal repository for FinTablo API.
"""

from typing import Dict, Any, List
from ..base import BaseRepository
from ..models import Deal
from ..http_client import HttpClient


class DealRepository(BaseRepository[Deal]):
    """Repository for managing deals (сделки)."""
    
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/deal", Deal)
    
    def get_by_partner(self, partner_id: int) -> List[Deal]:
        """Get deals by partner."""
        params = {"partnerId": partner_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_status(self, status_id: int) -> List[Deal]:
        """Get deals by status."""
        params = {"statusId": status_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_direction(self, direction_id: int) -> List[Deal]:
        """Get deals by direction."""
        params = {"directionId": direction_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_responsible(self, responsible_id: int) -> List[Deal]:
        """Get deals by responsible person."""
        params = {"responsibleId": responsible_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def add_stage(self, deal_id: int, stage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a stage to a deal."""
        return self.http_client.post(f"/{self.endpoint}/{deal_id}/add-stage", data=stage_data)
    
    def _create_models_from_response(self, data: Dict[str, Any]) -> List[Deal]:
        """Create model instances from API response."""
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        else:
            items = data if isinstance(data, list) else [data]
        
        return [self._create_model(item) for item in items if item]