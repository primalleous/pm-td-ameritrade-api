from typing import overload

from td.models.rest.query import PriceHistoryQuery
from td.models.rest.response import PriceHistoryResponse
from td.session import TdAmeritradeSession
from td.utils.helpers import QueryInitializer


class PriceHistory:

    """
    ## Overview:
    ----
    Allows the user to query price history data for equity
    instruments.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `PriceHistory` services.

        Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.

        Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> price_history_service = td_client.price_history()
        """

        self.session = session

    @overload
    def get_price_history(self, **kwargs):  # This is here to get linter to shut up
        pass

    @QueryInitializer(PriceHistoryQuery)
    def get_price_history(self, price_history_query: PriceHistoryQuery) -> dict:
        """Gets historical candle data for a financial instrument.

        Documentation
        ----
        https://developer.tdameritrade.com/price-history/apis

        Parameters
        ----
        price_history_query : PriceHistoryQuery

        Usage
        ----
            1. Population by field names specified in `PriceHistoryQuery`
            >>> price_history_service = td_client.price_history()
            >>> price_history = price_history_service.get_price_history(
                    symbol="MSFT",
                    frequency_type=FrequencyType.DAILY,
                    frequency=1,
                    period_type=PeriodType.MONTH,
                    period=1,
                    extended_hours_needed=False,
                )
            2. Pass a dictionary with field names specified in `PriceHistoryQuery`
            >>> price_history = price_history_service.get_price_history({
                    "symbol": "MSFT",
                    "frequency_type": FrequencyType.DAILY,
                    "frequency": 1,
                    "period_type": PeriodType.MONTH,
                    "period": 1,
                    "extended_hours_needed": False,
                })

            3. Pass an `PriceHistoryQuery` object directly
            >>> price_history_query = PriceHistoryQuery(**{
                    "symbol": "MSFT",
                    "frequency_type": FrequencyType.DAILY,
                    "frequency": 1,
                    "period_type": PeriodType.MONTH,
                    "period": 1,
                    "extended_hours_needed": False,
                })
            >>> price_history = price_history_service.get_price_history(price_history_query)
        """

        res = self.session.make_request(
            method="get",
            endpoint=f"marketdata/{price_history_query.symbol}/pricehistory",
            params=price_history_query.model_dump(mode="json", by_alias=True),
        )

        if res:
            return PriceHistoryResponse(**res)
        else:
            return {}
