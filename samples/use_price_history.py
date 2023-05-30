from pprint import pprint
from td.client import TdAmeritradeClient
from td.enums.enums import PeriodType
from td.enums.enums import FrequencyType
from datetime import datetime
from datetime import timedelta

from td.models.rest.query import PriceHistoryQuery

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `PriceHistory` service.
price_history_service = td_client.price_history()

# Grab the Price History, with enums.
price_history = price_history_service.get_price_history(
    symbol="MSFT",
    frequency_type=FrequencyType.DAILY,
    frequency=1,
    period_type=PeriodType.MONTH,
    period=1,
    extended_hours_needed=True,
)
pprint(price_history)

price_history = price_history_service.get_price_history(
    {
        "symbol": "MSFT",
        "frequency_type": FrequencyType.DAILY,
        "frequency": 1,
        "period_type": PeriodType.MONTH,
        "period": 1,
        "extended_hours_needed": False,
    }
)
pprint(price_history)

price_history_query = PriceHistoryQuery(
    **{
        "symbol": "MSFT",
        "frequency_type": FrequencyType.DAILY,
        "frequency": 1,
        "period_type": PeriodType.MONTH,
        "period": 1,
        "extended_hours_needed": False,
    }
)

pprint(price_history_service.get_price_history(price_history_query))

# The max look back period for minute data is 31 Days.
end_date = datetime.now()
start_date = datetime.now() - timedelta(days=31)

# Grab the Price History, custom time frame.
price_history = price_history_service.get_price_history(
    symbol="MSFT",
    frequency_type=FrequencyType.MINUTE,
    frequency=1,
    start_date=start_date,
    end_date=end_date,
    extended_hours_needed=True,
)
print(len(price_history.candles))
