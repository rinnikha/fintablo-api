"""
Tests for repository classes.
"""

import pytest
from unittest.mock import Mock
from fintablo_api.repositories import AccountRepository, TransactionRepository, Account, Transaction


class TestAccountRepository:
    """Test cases for AccountRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_http_client = Mock()
        self.repository = AccountRepository(self.mock_http_client)
    
    def test_repository_initialization(self):
        """Test repository initialization."""
        assert self.repository.endpoint == "accounts"
        assert self.repository.model_class == Account
    
    def test_get_by_type(self):
        """Test getting accounts by type."""
        mock_data = [
            {"id": "1", "name": "Test Account", "type": "checking", "balance": 1000.0},
            {"id": "2", "name": "Another Account", "type": "checking", "balance": 2000.0}
        ]
        self.mock_http_client.get.return_value = mock_data
        
        accounts = self.repository.get_by_type("checking")
        
        self.mock_http_client.get.assert_called_once()
        assert len(accounts) == 2
        assert all(isinstance(account, Account) for account in accounts)
    
    def test_get_active_accounts(self):
        """Test getting active accounts."""
        mock_data = [{"id": "1", "name": "Active Account", "status": "active"}]
        self.mock_http_client.get.return_value = mock_data
        
        accounts = self.repository.get_active_accounts()
        
        assert len(accounts) == 1
        assert accounts[0].status == "active"


class TestTransactionRepository:
    """Test cases for TransactionRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_http_client = Mock()
        self.repository = TransactionRepository(self.mock_http_client)
    
    def test_repository_initialization(self):
        """Test repository initialization."""
        assert self.repository.endpoint == "/v1/transactions"
        assert self.repository.model_class == Transaction
    
    def test_get_by_account(self):
        """Test getting transactions by account."""
        mock_data = [
            {"id": "1", "account_id": "acc1", "amount": 100.0, "description": "Test transaction"}
        ]
        self.mock_http_client.get.return_value = mock_data
        
        transactions = self.repository.get_by_account("acc1")
        
        assert len(transactions) == 1
        assert transactions[0].account_id == "acc1"
    
    def test_get_recent(self):
        """Test getting recent transactions."""
        mock_data = [
            {"id": "1", "amount": 100.0, "created_at": "2023-01-01T00:00:00Z"}
        ]
        self.mock_http_client.get.return_value = mock_data
        
        transactions = self.repository.get_recent(limit=5)
        
        assert len(transactions) == 1


class TestModels:
    """Test cases for model classes."""
    
    def test_account_model(self):
        """Test Account model."""
        data = {
            "id": "acc1",
            "name": "Test Account",
            "type": "checking",
            "balance": 1000.0,
            "currency": "USD"
        }
        
        account = Account(data)
        
        assert account.id == "acc1"
        assert account.name == "Test Account"
        assert account.balance == 1000.0
        assert account.to_dict() == data
    
    def test_transaction_model(self):
        """Test Transaction model."""
        data = {
            "id": "txn1",
            "account_id": "acc1",
            "amount": 100.0,
            "type": "credit",
            "description": "Test transaction"
        }
        
        transaction = Transaction(data)
        
        assert transaction.id == "txn1"
        assert transaction.account_id == "acc1"
        assert transaction.amount == 100.0
        assert transaction.to_dict() == data