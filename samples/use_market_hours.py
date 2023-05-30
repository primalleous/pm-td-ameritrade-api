from pprint import pprint
from datetime import datetime
from td.client import TdAmeritradeClient
from td.enums.enums import Markets
from td.models.rest.query import MarketHoursQuery


# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `MarketHours` service.
market_hours_service = td_client.market_hours()

# Grab the hours for a specific market.
pprint(
    market_hours_service.get_market_hours(markets="EQUITY", date_time=datetime.now())
)


market_hours_query = MarketHoursQuery(markets="EQUITY", date_time=datetime.now())
pprint(market_hours_service.get_market_hours(market_hours_query))


pprint(
    market_hours_service.get_market_hours(
        {"markets": "EQUITY", "date_time": datetime.now()}
    )
)


# Grab the market hours
pprint(
    market_hours_service.get_multiple_market_hours(
        markets=["EQUITY", Markets.BOND], date_time=datetime.now()
    )
)

market_hours_query = MarketHoursQuery(markets="EQUITY,BOND", date_time=datetime.now())
pprint(market_hours_service.get_multiple_market_hours(market_hours_query))
