import json

from rich import print_json

from td.client import TdAmeritradeClient
from td.config import TdConfiguration
from td.models.rest.response import SecuritiesAccount, Transaction

# A config object
config = TdConfiguration()


# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

account_number = config.accounts.default_account

# Initialize the `Accounts` service.
accounts_service = td_client.accounts()


# Single Account

accounts = accounts_service.get_accounts(
    account_id=account_number, include_positions=True, include_orders=True
)

if not isinstance(accounts, SecuritiesAccount):
    accounts_json = json.dumps(accounts)
    print_json(accounts_json)
else:
    print_json(accounts.json(exclude_none=True))


# # All Accounts

accounts = accounts_service.get_accounts()

if not isinstance(accounts, SecuritiesAccount) and not isinstance(accounts, list):
    accounts_json = json.dumps(accounts)
    print_json(accounts_json)
else:
    if isinstance(accounts, list):
        for account in accounts:
            print_json(account.json(exclude_none=True))


# All Transactions

transactions = accounts_service.get_transactions(account_number)


if not isinstance(transactions, Transaction) and not isinstance(transactions, list):
    transactions_json = json.dumps(transactions)
    print_json(transactions_json)
else:
    if isinstance(transactions, list):
        for transaction in transactions:
            print_json(transaction.json(exclude_none=True))


# Single Transaction

transactions = accounts_service.get_transaction(account_number, "50168166480")

if not isinstance(transactions, Transaction) and not isinstance(transactions, list):
    transactions_json = json.dumps(transactions)
    print_json(transactions_json)
else:
    if isinstance(transactions, list):
        for transaction in transactions:
            print_json(transaction.json(exclude_none=True))
