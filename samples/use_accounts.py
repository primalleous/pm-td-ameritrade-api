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

transactions = accounts_service.get_transactions(
    "232773952", start_date="2023-12-07", end_date="2023-12-16"
)

if not isinstance(transactions, Transaction) and not isinstance(transactions, list):
    transactions_json = json.dumps(transactions)
    print_json(transactions_json)
else:
    if isinstance(transactions, list):
        for transaction in transactions:
            if isinstance(transaction, Transaction):
                print_json(transaction.model_dump_json(exclude_none=True))
            else:
                transaction_json = json.dumps(transaction)
                print_json(transaction_json)


# Single Account

accounts = accounts_service.get_accounts(
    account_id=account_number, include_positions=True, include_orders=True
)

if not isinstance(accounts, SecuritiesAccount):
    accounts_json = json.dumps(accounts)
    print_json(accounts_json)
else:
    print_json(accounts.model_dump_json(exclude_none=True))


# # All Accounts

accounts = accounts_service.get_accounts()

if not isinstance(accounts, SecuritiesAccount) and not isinstance(accounts, list):
    accounts_json = json.dumps(accounts)
    print_json(accounts_json)
else:
    if isinstance(accounts, list):
        for account in accounts:
            if isinstance(account, SecuritiesAccount):
                print_json(account.model_dump_json(exclude_none=True))
            else:
                account_json = json.dumps(account)
                print_json(account_json)

# # All Transactions

transactions = accounts_service.get_transactions(account_number)


if not isinstance(transactions, Transaction) and not isinstance(transactions, list):
    transactions_json = json.dumps(transactions)
    print_json(transactions_json)
else:
    if isinstance(transactions, list):
        for transaction in transactions:
            if isinstance(transaction, Transaction):
                print_json(transaction.model_dump_json(exclude_none=True))
            else:
                transaction_json = json.dumps(transaction)
                print_json(transaction_json)


# Single Transaction

transactions = accounts_service.get_transaction(account_number, "50168166480")
print(type(transactions))
print(transactions)

if not isinstance(transactions, Transaction) and not isinstance(transactions, list):
    transactions_json = json.dumps(transactions)
    print_json(transactions_json)
elif isinstance(transactions, list):
    for transaction in transactions:
        if isinstance(transaction, Transaction):
            print_json(transaction.model_dump_json(exclude_none=True))
        else:
            transaction_json = json.dumps(transaction)
            print_json(transaction_json)
elif isinstance(transactions, Transaction):
    print_json(transactions.model_dump_json(exclude_none=True))
