import json
from datetime import datetime

from rich import print as rprint
from rich import print_json

from td.client import TdAmeritradeClient
from td.config import TdConfiguration
from td.models.orders import Order

# A config object
config = TdConfiguration("config-example/config.ini")

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

account_number = config.accounts.default_account

# Initialize the `Orders` service.
orders_service = td_client.orders()


# Query or Path

order_query = orders_service.get_orders_by_query(
    account_number,
    from_entered_time="2024-01-12",
    to_entered_time=datetime.today().date().isoformat(),
)

for order in order_query:
    if not isinstance(order, Order):
        order_json = json.dumps(order)
        print_json(order_json)
    else:
        print_json(order.model_dump_json(exclude_none=True))


order_path = orders_service.get_orders_by_path(
    account_number,
    from_entered_time="2024-01-12",
    to_entered_time=datetime.today().date().isoformat(),
    order_status="WORKING",
)

for order in order_path:
    if not isinstance(order, Order):
        order_json = json.dumps(order)
        print_json(order_json)
    else:
        print_json(order.model_dump_json(exclude_none=True))


# Get specific order

order = orders_service.get_order(account_number, order_id="6238637007")

if not isinstance(order, Order):
    order_json = json.dumps(order)
    print_json(order_json)
else:
    print_json(order.model_dump_json(by_alias=True, exclude_none=True))


# Cancel Order

order_cancel = orders_service.cancel_order(account_number, order_id="6238634928")

rprint(order_cancel)
