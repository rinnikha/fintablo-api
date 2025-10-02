"""
Partner repository for FinTablo API.
"""

from typing import Dict, Any, List
from ..base import BaseRepository
from ..models import Partner
from ..http_client import HttpClient


class PartnerRepository(BaseRepository[Partner]):
    """Repository for managing partners (контрагенты)."""
    
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client, "v1/partner", Partner)
    
    def search_by_name(self, name: str) -> List[Partner]:
        """Search partners by name."""
        params = {"name": name}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_inn(self, inn: str) -> List[Partner]:
        """Get partners by INN."""
        params = {"inn": inn}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def get_by_group(self, group_id: int) -> List[Partner]:
        """Get partners by group ID."""
        params = {"groupId": group_id}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def search_by_comment(self, comment: str) -> List[Partner]:
        """Search partners by comment."""
        params = {"comment": comment}
        data = self.http_client.get(f"/{self.endpoint}", params=params)
        return self._create_models_from_response(data)
    
    def _create_models_from_response(self, data: Dict[str, Any]) -> List[Partner]:
        """Create model instances from API response."""
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        else:
            items = data if isinstance(data, list) else [data]
        
        return [self._create_model(item) for item in items if item]