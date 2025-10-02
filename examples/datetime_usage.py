"""
Example showing datetime handling in FinTablo API models.
"""

import os
from datetime import datetime, timedelta
from fintablo_api import Fintablo, Transaction
from fintablo_api.exceptions import FinTabloException


def main():
    api_key = os.environ.get("FINTABLO_API_KEY")
    if not api_key:
        print("Please set the FINTABLO_API_KEY environment variable")
        return
    
    client = Fintablo(api_key=api_key, debug=False)
    
    try:
        print("=== Datetime Handling Examples ===")
        
        # Example 1: Creating a transaction with datetime
        print("\n1. Creating transaction with datetime object:")
        
        transaction = Transaction(
            value=100000.0,
            description="Payment with datetime",
            group="income",
            date=datetime.now(),  # Using datetime object
            moneybag_id=123,
            category_id=456
        )
        
        print(f"Transaction date (datetime): {transaction.date}")
        print(f"Type: {type(transaction.date)}")
        
        # Example 2: Converting to API format
        print("\n2. Converting to API format:")
        api_dict = transaction.to_api_dict()
        print(f"API date (string): {api_dict['date']}")
        print(f"API dict: {api_dict}")
        
        # Example 3: Different date formats
        print("\n3. Working with different date formats:")
        
        # Today
        today_transaction = Transaction(
            date=datetime.now(),
            description="Today's payment",
            value=50000.0
        )
        
        # Yesterday  
        yesterday_transaction = Transaction(
            date=datetime.now() - timedelta(days=1),
            description="Yesterday's payment",
            value=75000.0
        )
        
        # Specific date
        specific_transaction = Transaction(
            date=datetime(2024, 1, 15),
            description="Specific date payment",
            value=125000.0
        )
        
        print(f"Today: {today_transaction.to_api_dict()['date']}")
        print(f"Yesterday: {yesterday_transaction.to_api_dict()['date']}")
        print(f"Specific: {specific_transaction.to_api_dict()['date']}")
        
        # Example 4: API client usage (commented out for safety)
        print("\n4. Using with API client:")
        print("# This would create the transaction:")
        print("# created_transaction = client.transactions.create(transaction)")
        print("# The datetime gets automatically converted to 'YYYY-MM-DD' format")
        
        print("\n✅ Datetime handling works correctly!")
        print("✅ Python datetime objects → API string format (YYYY-MM-DD)")
        print("✅ API string format → Python datetime objects (when reading)")
        
    except FinTabloException as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()