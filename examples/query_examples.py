"""
Advanced query examples for the Fintablo API client.
"""

import os
from datetime import datetime, timedelta
from fintablo_api import Fintablo
from fintablo_api.models import Transaction


def main():
    api_key = os.environ.get("FINTABLO_API_KEY")
    if not api_key:
        print("Please set the FINTABLO_API_KEY environment variable")
        return
    
    client = Fintablo(api_key=api_key, debug=True)
    
    try:
        print("=== Advanced FinTablo API Query Examples ===")
        
        # Example 1: Categories by group
        print("\n1. Categories by group:")
        income_categories = client.categories.get_income_categories()
        outcome_categories = client.categories.get_outcome_categories()
        
        print(f"Found {len(income_categories)} income categories")
        print(f"Found {len(outcome_categories)} outcome categories")
        
        # Example 2: Accounts by type
        print("\n2. Accounts by type:")
        cash_accounts = client.moneybags.get_cash_accounts()
        bank_accounts = client.moneybags.get_bank_accounts()
        
        print(f"Cash accounts: {len(cash_accounts)}")
        print(f"Bank accounts: {len(bank_accounts)}")

        # Example: Create a new transaction using the improved model
        new_transaction = Transaction(
            category_id=income_categories[0].id,
            date=datetime.now().strftime("%Y-%m-%d"),
            moneybag_id=cash_accounts[0].id,
            value=200000.5,
            description="test1",
            group="income"
        )
        
        created_transaction = client.transactions.create(new_transaction)
        print(f"Created transaction: {created_transaction.description} - {created_transaction.value}")
        
        for account in cash_accounts[:3]:
            print(f"- Cash: {account.name} ({account.balance or 0} {account.currency or 'RUB'})")
        
        # Example 3: Date range transaction query
        print("\n3. Transactions from last 30 days:")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        recent_transactions = client.transactions.get_by_date_range(start_date, end_date)
        print(f"Found {len(recent_transactions)} transactions in the last 30 days")
        
        # Example 4: Transaction filtering by type
        print("\n4. Transaction filtering by group:")
        income_transactions = client.transactions.get_income_transactions()[:5]
        outcome_transactions = client.transactions.get_outcome_transactions()[:5]
        
        print(f"Income transactions: {len(income_transactions)}")
        for txn in income_transactions:
            print(f"- Income: {txn.description or 'No description'}: +{txn.value}")
            
        print(f"Outcome transactions: {len(outcome_transactions)}")
        for txn in outcome_transactions:
            print(f"- Outcome: {txn.description or 'No description'}: -{txn.value}")
        
        # Example 5: Partner operations
        print("\n5. Partner operations:")
        partners = client.partners.find_all()[:5]
        
        for partner in partners:
            print(f"Partner: {partner.name}")
            # Get transactions for this partner
            partner_transactions = client.transactions.get_by_partner(partner.id)
            print(f"  - Has {len(partner_transactions)} transactions")
        
        # Example 6: Deal analysis
        print("\n6. Deal analysis:")
        deals = client.deals.find_all()[:3]
        
        for deal in deals:
            print(f"Deal: {deal.name}")
            print(f"  - Amount: {deal.amount or 0} {deal.currency or 'RUB'}")
            
            # Get transactions for this deal
            deal_transactions = client.transactions.get_by_deal(deal.id)
            print(f"  - Transactions: {len(deal_transactions)}")
        
        # Example 7: Planned vs Actual transactions
        print("\n7. Planned vs Actual transactions:")
        planned = client.transactions.get_planned_transactions()
        actual = client.transactions.get_actual_transactions()
        
        print(f"Planned transactions: {len(planned)}")
        print(f"Actual transactions: {len(actual)}")
        
        # Example 8: Search operations
        print("\n8. Search operations:")
        
        # Search accounts by name
        test_accounts = client.moneybags.search_by_name("test")
        print(f"Accounts with 'test' in name: {len(test_accounts)}")
        
        # Search partners by name
        client_partners = client.partners.search_by_name("client")
        print(f"Partners with 'client' in name: {len(client_partners)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()