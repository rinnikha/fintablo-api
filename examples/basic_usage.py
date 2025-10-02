"""
Basic usage example for the Fintablo API client.
"""

import os
from datetime import datetime, timedelta
from fintablo_api import Fintablo
from fintablo_api.exceptions import FinTabloException
from fintablo_api.models import Transaction, GroupEnum


def main():
    # Initialize client
    api_key = os.environ.get("FINTABLO_API_KEY")
    if not api_key:
        print("Please set the FINTABLO_API_KEY environment variable")
        return

    client = Fintablo(api_key=api_key, debug=True)

    try:
        # Test connection
        print("Testing connection...")
        result = client.test_connection()
        print(f"Connection test: {'Success' if result['success'] else 'Failed'}")
        if not result["success"]:
            print(f"Error: {result['message']}")
            return

        # Example: Get all categories
        print("\nFetching categories...")
        categories = client.categories.get_income_categories()
        print(f"Found {len(categories)} income categories")

        for category in categories[:5]:  # Show first 5
            print(f"- {category.name} (ID: {category.id}, Group: {category.group})")

        # Example: Get all accounts (moneybags)
        print("\nFetching accounts...")
        accounts = client.moneybags.get_active_accounts()
        print(f"Found {len(accounts)} active accounts")

        new_transaction = Transaction(
            date=datetime.now(),
            categoryId=categories[0].id,
            moneybagId=accounts[0].id,
            value=200000,
            description="test1",
            group=GroupEnum.INCOME,
        )

        new_transaction = client.transactions.create(new_transaction)

        for account in accounts[:5]:  # Show first 5
            print(
                f"- {account.name} ({account.type}): {account.balance or 0} {account.currency or 'RUB'}"
            )

        # Example: Get transactions
        print("\nFetching recent transactions...")
        transactions = client.transactions.get_actual_transactions()[
            :10
        ]  # Get first 10 actual transactions
        print(f"Found {len(transactions)} transactions")

        for transaction in transactions[:5]:  # Show first 5
            print(
                f"- {transaction.description or 'No description'}: {transaction.value} (Group: {transaction.group})"
            )

        # Example: Get partners
        print("\nFetching partners...")
        partners = client.partners.find_all()[:5]  # Get first 5 partners
        print(f"Found {len(partners)} partners")

        for partner in partners:
            print(f"- {partner.name} (INN: {partner.inn or 'N/A'})")

        # Example: Filter transactions by account
        if accounts:
            account = accounts[0]
            print(f"\nFetching transactions for account: {account.name}")
            account_transactions = client.transactions.get_by_account(account.id)
            print(f"Found {len(account_transactions)} transactions for this account")

        # Example: Get deals
        print("\nFetching deals...")
        deals = client.deals.find_all()[:5]  # Get first 5 deals
        print(f"Found {len(deals)} deals")

        for deal in deals:
            print(f"- {deal.name}: {deal.amount or 0} {deal.currency or 'RUB'}")

    except FinTabloException as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
