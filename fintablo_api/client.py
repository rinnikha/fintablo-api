"""Main client class for the Fintablo API."""

import logging
from typing import Optional, Dict, Any

from .http_client import HttpClient
from .exceptions import FinTabloException, AuthenticationException
from .logging_utils import get_logger
from .repositories import (
    CategoryRepository,
    MoneybagRepository,
    TransactionRepository,
    PartnerRepository,
    DealRepository,
)


logger = get_logger("client")


class Fintablo:
    """
    Main client for interacting with the Fintablo API.
    
    This class provides access to various API endpoints through repository-style
    interfaces, following the pattern established in the MoySkald client.
    """
    
    DEFAULT_BASE_URL = "https://api.fintablo.ru/v1"
    DEFAULT_TIMEOUT = 30
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        debug: bool = False,
        user_agent: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Fintablo client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (defaults to DEFAULT_BASE_URL)
            timeout: Request timeout in seconds (defaults to DEFAULT_TIMEOUT)
            debug: Enable debug logging
            user_agent: Custom User-Agent header
            **kwargs: Additional arguments passed to HttpClient
        """
        if not api_key:
            raise AuthenticationException("API key is required")
        
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.debug = debug
        
        if debug:
            logger.setLevel(logging.DEBUG)
        
        # Initialize HTTP client
        self.http_client = HttpClient(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout,
            user_agent=user_agent,
            debug=debug,
            **kwargs
        )
        
        # Initialize repositories based on actual FinTablo API
        self.categories = CategoryRepository(self.http_client)
        self.moneybags = MoneybagRepository(self.http_client)
        self.transactions = TransactionRepository(self.http_client)
        self.partners = PartnerRepository(self.http_client)
        self.deals = DealRepository(self.http_client)
        
        # Aliases for convenience
        self.accounts = self.moneybags  # Alias for backward compatibility
        
        logger.info(f"Fintablo client initialized with base URL: {self.base_url}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close the HTTP session."""
        if hasattr(self.http_client, 'close'):
            self.http_client.close()
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection and authentication by fetching categories.
        
        Returns:
            Dict containing connection test results
        """
        try:
            # Test connection by fetching categories (always available endpoint)
            response = self.http_client.get("/v1/category")
            return {
                "success": True,
                "message": "Connection successful",
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "error": e
            }
