from td.enums.enums import Projections
from td.models.rest.query import InstrumentsQuery
from td.models.rest.response import (
    BaseInstrument,
    BondInstrument,
    InstrumentFundamental,
)
from td.session import TdAmeritradeSession
from td.utils.helpers import QueryInitializer


class Instruments:

    """
    ## Overview
    ----
    Allows the user to query and search for financial instruments
    inside of the TD Ameritrade database. The endpoint allows multiple
    methods for searching including regex.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Instruments` services.

        Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    @QueryInitializer(InstrumentsQuery)
    def search_instruments(self, instruments_query: InstrumentsQuery) -> dict:
        """Search or retrieve instrument data, including fundamental data.

        Documentation
        ----
        https://developer.tdameritrade.com/instruments/apis/get/instruments

        Parameters
        ----
        instruments_query : InstrumentsQuery

        Usage
        ----
            This method can be used in three different ways:

            1. Population by field names specified in `InstrumentsQuery`
            >>> instruments_service = td_client.instruments()
            >>> instruments_service.search_instruments(symbol='MSFT', projection='symbol-search')

            2. Pass a dictionary with field names specified in `InstrumentsQuery`
            >>> instruments_service.search_instruments({'symbol': 'MSFT', 'projection': 'symbol-search'})

            3. Pass an `InstrumentsQuery` object directly
            >>> instruments_query = InstrumentsQuery(symbol="MSFT", projection="symbol-search")
            >>> instruments_service.search_instruments(instruments_query)
        """
        res = self.session.make_request(
            method="get",
            endpoint="instruments",
            params=instruments_query.dict(by_alias=True),
        )

        if res:
            temp_dict = {}
            for symbol in res:
                instrument = res[symbol]
                if instruments_query.projection != Projections.FUNDAMENTAL.value:
                    if instrument["assetType"] == "BOND":
                        temp_dict[symbol] = BondInstrument(**instrument)
                    else:
                        temp_dict[symbol] = BaseInstrument(**instrument)
                else:
                    temp_dict[symbol] = InstrumentFundamental(**instrument)
            return temp_dict
        return {}

    def get_instrument(self, cusip: str) -> dict:
        """Get an instrument by CUSIP.

        Documentation
        ----
        https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D

        Parameters
        ----
        cusip: str
            The CUSIP Id.

        Usage
        ----
            >>> from td.enums import Instruments
            >>> instruments_service = td_client.instruments()
            >>> instruments_service.get_instrument(
                cusip='617446448'
            )
        """

        res = self.session.make_request(method="get", endpoint=f"instruments/{cusip}")

        if res:
            temp_dict = {}
            for asset in res:
                symbol = asset["symbol"]
                if asset["assetType"] == "BOND":
                    temp_dict[symbol] = BondInstrument(**asset)
                else:
                    temp_dict[symbol] = BaseInstrument(**asset)
            return temp_dict
        return {}
