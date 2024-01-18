from rich import print as rprint
from rich import print_json

from td.client import TdAmeritradeClient
from td.orders.options import OptionSymbol

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `Quotes` service.
quote_service = td_client.quotes()

# Single Quote

# EQUITY
rprint(quote_service.get_quote(instrument="AAPL"))

#  INDEX
rprint(quote_service.get_quote(instrument="$DJI"))

#  MUTUAL_FUND
rprint(quote_service.get_quote(instrument="VFIAX"))

# OPTION
option_symbol = OptionSymbol("SPY", "011624", "C", "480").build()
res = quote_service.get_quote(instrument=option_symbol)
if res:
    print_json(res[option_symbol].model_dump_json())

# ETF
rprint(quote_service.get_quote(instrument="SPY"))

# FOREX - not working for me
# rprint(quote_service.get_quote(instrument="EUR/USD"))

# FUTURE - not working for me
# rprint(quote_service.get_quote(instrument="/ES"))

# FUTURE_OPTION
# ...


# Multiple quotes.
res = quote_service.get_quotes(instruments=["SPY", "QQQ"])
if res:
    print_json(res["SPY"].model_dump_json())
    print()
    print_json(res["QQQ"].model_dump_json())
