from rich import print_json
from td.client import TdAmeritradeClient
from td.config import TdConfiguration
from td.enums.orders import Duration, OrderInstruction, OrderStrategyType, Session
from td.orders.builder import (
    OrderBuilder,
    first_triggers_second,
    one_triggers_one_cancels_other,
)
from td.orders.options import (
    OptionSymbol,
    option_buy_to_open_limit,
    option_sell_to_close_limit,
)

# A config object
config = TdConfiguration("config-example/config.ini")

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

account_number = config.accounts.default_account

# Initialize the `Orders` service.
orders_service = td_client.orders()

# These are good examples of how to use the OrderBuilder class in general

#  Substantial portions of order functions weren't written by me and haven't been fully
#  tested yet. See copyright in those files.

# I did rewrite the OrderBuilder class though and think builder pattern + function abstractions is the best way.
# More work needs to be done to abstract other types of orders out.

option_symbol = OptionSymbol("SPY", "053023", "P", "400").build()

# One Triggers a One Cancels Other

option_limit_buy_order = option_buy_to_open_limit(
    option_symbol, 1, 0.10
)  # DO NOT build here
option_limit_sell_order = option_sell_to_close_limit(
    option_symbol, 1, 0.2
)  # DO NOT build here
option_stop_limit_sell_to_close_order = (
    OrderBuilder()
    .set_session(Session.NORMAL)
    .set_duration(Duration.DAY)
    .set_order_type("LIMIT")
    .set_price(0.02)
    .set_order_strategy_type(OrderStrategyType.SINGLE)
    .add_option_leg(OrderInstruction.SELL_TO_CLOSE, option_symbol, 1)
    .build()  # Build Here
)

otoco = one_triggers_one_cancels_other(
    option_limit_buy_order,
    option_limit_sell_order,
    option_stop_limit_sell_to_close_order,
).build()
print_json(otoco.json(exclude_none=True))
# orders_service.place_order(account_number, otoco)


# First Triggers Second

option_market_buy_order = option_buy_to_open_limit(option_symbol, 1, 0.10)
option_market_sell_order = option_sell_to_close_limit(option_symbol, 1, 0.10).build()

fts = first_triggers_second(option_market_buy_order, option_market_sell_order).build()
print_json(fts.json(exclude_none=True))
# orders_service.place_order(account_number, fts)
