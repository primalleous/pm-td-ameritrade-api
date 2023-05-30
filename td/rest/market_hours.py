from td.models.rest.query import MarketHoursQuery
from td.models.rest.response import MarketHoursResponse
from td.session import TdAmeritradeSession
from td.utils.helpers import QueryInitializer


class MarketHours:

    """
    ## Overview
    ----
    Allows the user query the different market hours for
    the different financial markets.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `MarketHours` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    @QueryInitializer(MarketHoursQuery)
    def get_multiple_market_hours(self, market_hours_query: MarketHoursQuery) -> dict:
        """Returns the market hours for all the markets.

        ### Documentation
        ----
        https://developer.tdameritrade.com/market-hours/apis

        ### Parameters
        ----
        market_hours_query : MarketHoursQuery

        ### Usage
        ----
            1. Population by field names specified in `MarketHoursQuery`
            >>> market_hours_service = td_client.market_hours()
            >>> market_hours_service.get_multiple_market_hours(markets=["EQUITY", Markets.BOND], date_time=datetime.now())

            2. Pass a dictionary with field names specified in `MarketHoursQuery`
            >>> market_hours_service.get_multiple_market_hours({'markets': ["EQUITY", Markets.BOND], 'date_time': datetime.now()})

            3. Pass an `MarketHoursQuery` object directly
            >>> market_hours_query = MarketHoursQuery(markets="EQUITY,BOND", date_time=datetime.now())
            >>> market_hours_service.get_multiple_market_hours(market_hours_query)
        """
        res = self.session.make_request(
            method="get",
            endpoint="marketdata/hours",
            params=market_hours_query.dict(by_alias=True),
        )

        if res:
            temp_dict = {}
            for key in res.keys():
                for sub_key in res[key].keys():
                    temp_dict[res[key][sub_key]["marketType"]] = MarketHoursResponse(
                        **res[key][sub_key]
                    )
            return temp_dict
        return {}

    @QueryInitializer(MarketHoursQuery)
    def get_market_hours(self, market_hours_query: MarketHoursQuery) -> dict:
        """Returns the market hours for the specified market.

        ### Documentation
        ----
        https://developer.tdameritrade.com/market-hours/apis

        ### Parameters
        ----
        market_hours_query : MarketHoursQuery

        ### Usage
        ----
            1. Population by field names specified in `MarketHoursQuery`
            >>> market_hours_service = td_client.market_hours()
            >>> market_hours_service.get_market_hours(markets="EQUITY", date_time=datetime.now())

            2. Pass a dictionary with field names specified in `MarketHoursQuery`
            >>> market_hours_service.get_market_hours({'markets': 'EQUITY', 'date_time': datetime.now()})

            3. Pass an `MarketHoursQuery` object directly
            >>> market_hours_query = MarketHoursQuery(markets="EQUITY", date_time=datetime.now())
            >>> market_hours_service.get_market_hours(market_hours_query)
        """

        res = self.session.make_request(
            method="get",
            endpoint=f"marketdata/{market_hours_query.markets}/hours",
            params=market_hours_query.dict(by_alias=True),
        )

        if res:
            temp_dict = {}
            for key in res.keys():
                for sub_key in res[key].keys():
                    temp_dict[res[key][sub_key]["marketType"]] = MarketHoursResponse(
                        **res[key][sub_key]
                    )
            return temp_dict
        return {}
