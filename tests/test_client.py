"""
Tests for the Fintablo client.
"""

import pytest
from unittest.mock import Mock, patch
from fintablo_api import Fintablo
from fintablo_api.exceptions import AuthenticationException


class TestFinTabloClient:
    """Test cases for the main Fintablo client."""
    
    def test_client_initialization(self):
        """Test client initialization with valid API key."""
        client = Fintablo(api_key="test_key")
        
        assert client.api_key == "test_key"
        assert client.base_url == Fintablo.DEFAULT_BASE_URL
        assert client.timeout == Fintablo.DEFAULT_TIMEOUT
        assert hasattr(client, 'accounts')
        assert hasattr(client, 'transactions')
    
    def test_client_initialization_custom_params(self):
        """Test client initialization with custom parameters."""
        client = Fintablo(
            api_key="test_key",
            base_url="https://custom.api.url",
            timeout=60,
            debug=True
        )
        
        assert client.base_url == "https://custom.api.url"
        assert client.timeout == 60
        assert client.debug is True
    
    def test_client_initialization_no_api_key(self):
        """Test that initialization fails without API key."""
        with pytest.raises(AuthenticationException):
            Fintablo(api_key="")
        
        with pytest.raises(AuthenticationException):
            Fintablo(api_key=None)
    
    @patch('fintablo_api.client.HttpClient')
    def test_test_connection_success(self, mock_http_client):
        """Test successful connection test."""
        mock_client = Mock()
        mock_client.get.return_value = {"status": "ok"}
        mock_http_client.return_value = mock_client
        
        client = Fintablo(api_key="test_key")
        result = client.test_connection()
        
        assert result["success"] is True
        assert "Connection successful" in result["message"]
    
    @patch('fintablo_api.client.HttpClient')
    def test_test_connection_failure(self, mock_http_client):
        """Test connection test failure."""
        mock_client = Mock()
        mock_client.get.side_effect = Exception("Connection failed")
        mock_http_client.return_value = mock_client
        
        client = Fintablo(api_key="test_key")
        result = client.test_connection()
        
        assert result["success"] is False
        assert "Connection failed" in result["message"]
    
    def test_context_manager(self):
        """Test client as context manager."""
        with Fintablo(api_key="test_key") as client:
            assert client.api_key == "test_key"