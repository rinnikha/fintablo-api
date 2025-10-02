"""
HTTP client for making requests to the Fintablo API.
"""

import json
import logging
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    FinTabloException,
    AuthenticationException,
    NotFoundException,
    ValidationException,
    RateLimitException,
    ServerException,
    TimeoutException,
    ConnectionException,
)


logger = logging.getLogger(__name__)


class HttpClient:
    """HTTP client for making requests to the Fintablo API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        user_agent: Optional[str] = None,
        debug: bool = False,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.debug = debug
        
        # Create session
        self.session = requests.Session()
        
        # Set up retries
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=backoff_factor,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": user_agent or f"fintablo-api-python/0.1.0",
        })
        
        if debug:
            # Enable debug logging for requests
            logging.basicConfig(level=logging.DEBUG)
            logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Make an HTTP request to the API."""
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        
        # Prepare request arguments
        request_kwargs = {
            "timeout": self.timeout,
        }
        
        if params:
            request_kwargs["params"] = params
        
        if data:
            if isinstance(data, dict):
                request_kwargs["json"] = data
            else:
                request_kwargs["data"] = data
        
        if headers:
            request_kwargs["headers"] = {**self.session.headers, **headers}
        
        if self.debug:
            logger.debug(f"Making {method.upper()} request to {url}")
            if params:
                logger.debug(f"Query params: {params}")
            if data:
                logger.debug(f"Request data: {data}")
        
        try:
            response = self.session.request(method, url, **request_kwargs)
            
            if self.debug:
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
            
            self._handle_response_errors(response)
            return response
            
        except requests.exceptions.Timeout as e:
            raise TimeoutException(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionException(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise FinTabloException(f"Request failed: {str(e)}")
    
    def _handle_response_errors(self, response: requests.Response):
        """Handle HTTP error responses."""
        if response.status_code < 400:
            return
        
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown error")
        except (ValueError, json.JSONDecodeError):
            error_message = response.text or f"HTTP {response.status_code}"
        
        if response.status_code == 401:
            raise AuthenticationException(
                error_message,
                response=response,
                status_code=response.status_code
            )
        elif response.status_code == 404:
            raise NotFoundException(
                error_message,
                response=response,
                status_code=response.status_code
            )
        elif response.status_code == 422:
            errors = error_data.get("errors", []) if isinstance(error_data, dict) else []
            raise ValidationException(
                error_message,
                response=response,
                status_code=response.status_code,
                errors=errors
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitException(
                error_message,
                response=response,
                status_code=response.status_code,
                retry_after=retry_after
            )
        elif 500 <= response.status_code < 600:
            raise ServerException(
                error_message,
                response=response,
                status_code=response.status_code
            )
        else:
            raise FinTabloException(
                error_message,
                response=response,
                status_code=response.status_code
            )
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        response = self._make_request("GET", endpoint, params=params, **kwargs)
        return response.json() if response.content else {}
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        response = self._make_request("POST", endpoint, data=data, **kwargs)
        return response.json() if response.content else {}
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        response = self._make_request("PUT", endpoint, data=data, **kwargs)
        return response.json() if response.content else {}
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a PATCH request."""
        response = self._make_request("PATCH", endpoint, data=data, **kwargs)
        return response.json() if response.content else {}
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        response = self._make_request("DELETE", endpoint, **kwargs)
        return response.json() if response.content else {}
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()