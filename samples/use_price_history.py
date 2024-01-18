from datetime import datetime, timedelta

from rich import print as rprint

from td.client import TdAmeritradeClient
from td.enums.enums import FrequencyType, PeriodType
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
    need_extended_hours_data=True,
)
rprint(price_history)

price_history = price_history_service.get_price_history(
    {
        "symbol": "MSFT",
        "frequency_type": FrequencyType.DAILY,
        "frequency": 1,
        "period_type": PeriodType.MONTH,
        "period": 1,
        "need_extended_hours_data": False,
    }
)
rprint(price_history)

price_history_query = PriceHistoryQuery(
    **{
        "symbol": "MSFT",
        "frequency_type": FrequencyType.MINUTE,
        "frequency": 1,
        "period_type": PeriodType.DAY,
        "period": 1,
        "need_extended_hours_data": False,
    }
)

rprint(price_history_service.get_price_history(price_history_query=price_history_query))

# rprint(price_history_service.get_price_history(price_history_query))


# The max look back period for minute data is 31 Days.
end_date = datetime.now()
start_date = datetime.now() - timedelta(days=31)

price_history_query = PriceHistoryQuery(
    **{
        "symbol": "MSFT",
        "frequency_type": FrequencyType.MINUTE,
        "frequency": 1,
        "start_date": start_date,
        "end_date": end_date,
        "need_extended_hours_data": True,
    }
)

# Grab the Price History, custom time frame.
price_history = price_history_service.get_price_history(price_history_query)
print(len(price_history.candles))
