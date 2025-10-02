"""
Base classes for repositories and query builders.
"""

from typing import Dict, Any, List, Optional, Type, TypeVar, Generic

from .http_client import HttpClient


T = TypeVar("T")


class QueryBuilder(Generic[T]):
    """Base query builder for constructing API queries."""

    def __init__(self, repository: "BaseRepository"):
        self.repository = repository
        self._filters = {}
        self._ordering = []
        self._limit_value = None
        self._offset_value = None
        self._expand = []

    def filter(self, **kwargs) -> "QueryBuilder[T]":
        """Add filters to the query."""
        self._filters.update(kwargs)
        return self

    def order_by(self, field: str, ascending: bool = True) -> "QueryBuilder[T]":
        """Add ordering to the query."""
        direction = "asc" if ascending else "desc"
        self._ordering.append(f"{field}:{direction}")
        return self

    def limit(self, limit: int) -> "QueryBuilder[T]":
        """Set query limit."""
        self._limit_value = limit
        return self

    def offset(self, offset: int) -> "QueryBuilder[T]":
        """Set query offset."""
        self._offset_value = offset
        return self

    def expand(self, *fields: str) -> "QueryBuilder[T]":
        """Add fields to expand in the response."""
        self._expand.extend(fields)
        return self

    def build_params(self) -> Dict[str, Any]:
        """Build query parameters."""
        params = {}

        # Add filters
        params.update(self._filters)

        # Add ordering
        if self._ordering:
            params["order"] = ",".join(self._ordering)

        # Add pagination
        if self._limit_value is not None:
            params["limit"] = self._limit_value

        if self._offset_value is not None:
            params["offset"] = self._offset_value

        # Add expand
        if self._expand:
            params["expand"] = ",".join(self._expand)

        return params

    def execute(self) -> List[T]:
        """Execute the query and return results."""
        return self.repository._query_execute(self)

    def first(self) -> Optional[T]:
        """Get the first result."""
        results = self.limit(1).execute()
        return results[0] if results else None

    def count(self) -> int:
        """Get the count of results."""
        return self.repository._query_count(self)


class BaseRepository(Generic[T]):
    """Base repository class for API entities."""

    def __init__(self, http_client: HttpClient, endpoint: str, model_class: Type[T]):
        self.http_client = http_client
        self.endpoint = endpoint.strip("/")
        self.model_class = model_class

    def query(self) -> QueryBuilder[T]:
        """Create a new query builder."""
        return QueryBuilder(self)

    def find_all(self) -> List[T]:
        """Get all entities."""
        data = self.http_client.get(f"/{self.endpoint}")
        return self._create_models_from_response(data)

    def find_by_id(self, entity_id: int) -> Optional[T]:
        """Find an entity by ID."""
        try:
            data = self.http_client.get(f"/{self.endpoint}/{entity_id}")
            return self._create_model(data)
        except Exception:
            return None

    def create(self, entity: T) -> T:
        """Create a new entity."""
        # Convert model to API format
        if hasattr(entity, "to_api_dict"):
            data = entity.to_api_dict()
        elif hasattr(entity, "to_dict"):
            data = entity.to_dict()
        else:
            data = entity

        response_data = self.http_client.post(f"/{self.endpoint}", data=data)
        return self._create_model(response_data["items"][0])

    def update(self, entity_id: int, entity: T) -> T:
        """Update an existing entity."""
        # Convert model to API format
        if hasattr(entity, "to_api_dict"):
            data = entity.to_api_dict()
        elif hasattr(entity, "to_dict"):
            data = entity.to_dict()
        else:
            data = entity

        response_data = self.http_client.put(f"/{self.endpoint}/{entity_id}", data=data)
        return self._create_model(response_data["items"][0])

    def delete(self, entity_id: int) -> bool:
        """Delete an entity."""
        try:
            self.http_client.delete(f"/{self.endpoint}/{entity_id}")
            return True
        except Exception:
            return False

    def _query_execute(self, query_builder: QueryBuilder[T]) -> List[T]:
        """Execute a query and return results."""
        params = query_builder.build_params()
        data = self.http_client.get(f"/{self.endpoint}", params=params)

        # Handle different response formats
        if isinstance(data, dict):
            items = data.get("items", data.get("results", [data]))
        else:
            items = data if isinstance(data, list) else [data]

        return [self._create_model(item) for item in items if item]

    def _query_count(self, query_builder: QueryBuilder[T]) -> int:
        """Get count for a query."""
        params = query_builder.build_params()
        params["count"] = True
        data = self.http_client.get(f"/{self.endpoint}/count", params=params)
        return data.get("count", 0) if isinstance(data, dict) else 0

    def _create_model(self, data: Dict[str, Any]) -> T:
        """Create a model instance from API data."""
        if self.model_class == dict:
            return data

        # API data is already in camelCase, model fields are now camelCase too
        converted_data = {}
        for key, value in data.items():
            # Handle datetime conversion for date fields
            if key == "date" and value and isinstance(value, str):
                try:
                    from datetime import datetime

                    # Try to parse the date string to datetime
                    if len(value) == 10 and "-" in value:  # YYYY-MM-DD format
                        converted_data[key] = datetime.strptime(value, "%Y-%m-%d")
                    elif "." in value and len(value) >= 10:  # dd.mm.YYYY or dd.mm.YYYY HH:mm format
                        if len(value) == 10:  # dd.mm.YYYY
                            converted_data[key] = datetime.strptime(value, "%d.%m.%Y")
                        else:  # dd.mm.YYYY HH:mm
                            converted_data[key] = datetime.strptime(value, "%d.%m.%Y %H:%M")
                    else:
                        converted_data[key] = value
                except ValueError:
                    # If parsing fails, keep as string
                    converted_data[key] = value
            else:
                converted_data[key] = value

        try:
            result = self.model_class(**converted_data)
            return result
        except Exception as e:
            print(f"Error creating model: {e}")
            print(f"Model class: {self.model_class}")
            print(f"API data keys: {list(data.keys())}")
            print(
                f"Expected model fields: {list(self.model_class.__annotations__.keys()) if hasattr(self.model_class, '__annotations__') else 'unknown'}"
            )
            raise

    def _create_models_from_response(self, data: Dict[str, Any]) -> List[T]:
        """Create model instances from API response."""
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        else:
            items = data if isinstance(data, list) else [data]

        return [self._create_model(item) for item in items if item]
