from datetime import datetime

from rich import print as rprint

from td.client import TdAmeritradeClient
from td.enums.enums import Markets
from td.models.rest.query import MarketHoursQuery

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `MarketHours` service.
market_hours_service = td_client.market_hours()

# Grab the hours for a specific market.
rprint(
    market_hours_service.get_market_hours(markets="EQUITY", date_time=datetime.now())
)


market_hours_query = MarketHoursQuery(markets="EQUITY", date_time=datetime.now())
rprint(market_hours_service.get_market_hours(market_hours_query))


rprint(
    market_hours_service.get_market_hours(
        {"markets": "EQUITY", "date_time": datetime.now()}
    )
)


# Grab the market hours
rprint(
    market_hours_service.get_multiple_market_hours(
        markets=["EQUITY", Markets.BOND], date_time=datetime.now()
    )
)

market_hours_query = MarketHoursQuery(markets="EQUITY,BOND", date_time=datetime.now())
rprint(market_hours_service.get_multiple_market_hours(market_hours_query))
