from pprint import pprint
from td.client import TdAmeritradeClient

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `Quotes` service.
quote_service = td_client.quotes()

# Single Quote

# EQUITY
pprint(quote_service.get_quote(instrument="AAPL"))

#  INDEX
pprint(quote_service.get_quote(instrument="$DJI"))

#  MUTUAL_FUND
pprint(quote_service.get_quote(instrument="VFIAX"))

# OPTION
pprint(quote_service.get_quote(instrument="SPY_053023P421"))

# ETF
pprint(quote_service.get_quote(instrument="SPY"))

# # FOREX - not working for me
# # pprint(quote_service.get_quote(instrument="EUR/USD"))

# # FUTURE - not working for me
# # pprint(quote_service.get_quote(instrument="/ES"))

# # FUTURE_OPTION
# # ...


# Multiple quotes.
pprint(quote_service.get_quotes(instruments=["AAPL", "SQ"]))
