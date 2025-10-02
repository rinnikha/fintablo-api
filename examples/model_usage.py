"""
Model usage examples showing the clean dataclass-based FinTablo API models.
"""

import os
from datetime import datetime
from fintablo_api import Fintablo, Transaction, Category, Moneybag, Partner, Deal


def main():
    api_key = os.environ.get("FINTABLO_API_KEY")
    if not api_key:
        print("Please set the FINTABLO_API_KEY environment variable")
        return
    
    client = Fintablo(api_key=api_key, debug=False)  # Set to False for cleaner output
    
    try:
        print("=== Clean Dataclass Model Usage (Like MoySkald) ===")
        
        # Example 1: Creating models - clean and simple!
        print("\n1. Creating models with dataclasses (MoySkald style):")
        
        # Create a transaction - super clean!
        transaction = Transaction(
            value=150000.0,
            description="Payment from client",
            group="income",
            date=datetime.now().strftime("%Y-%m-%d"),
            moneybag_id=123,
            category_id=456
        )
        
        print(f"Transaction: {transaction}")
        print(f"API format: {transaction.to_api_dict()}")
        
        # Create other entities - just like MoySkald
        category = Category(
            name="Software Development",
            group="income",
            type="operating"
        )
        
        account = Moneybag(
            name="Main Business Account",
            type="bank",
            currency="RUB",
            balance=500000.0
        )
        
        partner = Partner(
            name="Tech Solutions LLC",
            inn="1234567890"
        )
        
        deal = Deal(
            name="Website Development Project",
            amount=300000.0,
            currency="RUB",
            partner_id=1
        )
        
        print(f"\nCategory: {category.name} ({category.group})")
        print(f"Account: {account.name} - {account.balance} {account.currency}")
        print(f"Partner: {partner.name}")
        print(f"Deal: {deal.name} - {deal.amount} {deal.currency}")
        
        # Example 2: Direct property access and modification
        print("\n2. Direct property access and modification:")
        
        # Modify properties directly
        transaction.value = 175000.0
        transaction.description = "Updated payment amount"
        account.balance = 600000.0
        
        print(f"Updated transaction: {transaction.description} - {transaction.value}")
        print(f"Updated account balance: {account.balance}")
        
        # Example 3: Using with API client
        print("\n3. Using with API client:")
        print("# These would make actual API calls:")
        print("# created_category = client.categories.create(category)")
        print("# created_account = client.moneybags.create(account)")  
        print("# created_partner = client.partners.create(partner)")
        print("# created_deal = client.deals.create(deal)")
        print("# created_transaction = client.transactions.create(transaction)")
        
        # Example 4: API conversion happens automatically
        print("\n4. Automatic API field conversion:")
        print("Python field: moneybag_id -> API field: moneybagId")
        print("Python field: category_id -> API field: categoryId")
        print("Python field: parent_id -> API field: parentId")
        
        sample_api_dict = transaction.to_api_dict()
        print(f"Contains 'moneybagId': {'moneybagId' in sample_api_dict}")
        print(f"Contains 'categoryId': {'categoryId' in sample_api_dict}")
        
        print("\n✅ Models are now clean, simple dataclasses like MoySkald!")
        print("✅ Easy to create: Transaction(value=100, description='test')")
        print("✅ Easy to modify: transaction.value = 200")
        print("✅ Automatic API conversion: snake_case ↔ camelCase")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()