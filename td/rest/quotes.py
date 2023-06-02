from typing import List
from td.models.rest.response import (
    ETFQuote,
    EquityQuote,
    ForexQuote,
    FutureQuote,
    FutureOptionsQuote,
    IndexQuote,
    MutualFundQuote,
    OptionQuote,
)
from td.session import TdAmeritradeSession


class Quotes:

    """
    ## Overview
    ----
    Allows the user to query real-time quotes from the TD
    API if they have an authorization token otherwise it
    will be delayed by 5 minutes.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Quotes` services.

        Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    def get_quote(self, instrument=str) -> dict:
        """Grabs real-time quotes for an instrument.

        Overview
        ----
        Serves as the mechanism to make a request to the Get
        Quote and Get Quotes Endpoint. If one item is provided
        a Get Quote request will be made and if more than one
        item is provided then a Get Quotes request will be made.

        Documentation
        ----
        https://developer.tdameritrade.com/quotes/apis

        Parameters
        ----
        instruments: str
            A list of different financial instruments.

        Usage
        ----
            >>> quote_service = td_client.quotes()
            >>> quote_service.get_quote(instrument='AAPL')
        """

        res = self.session.make_request(
            method="get", endpoint=f"marketdata/{instrument}/quotes"
        )

        if res:
            # return res
            for symbol in res:
                asset_type = res[symbol]["assetType"]
                match asset_type:
                    case "EQUITY":
                        res[symbol] = EquityQuote(**res[symbol])
                    case "INDEX":
                        res[symbol] = IndexQuote(**res[symbol])
                    case "MUTUAL_FUND":
                        res[symbol] = MutualFundQuote(**res[symbol])
                    case "OPTION":
                        res[symbol] = OptionQuote(**res[symbol])
                    case "FOREX":
                        res[symbol] = ForexQuote(**res[symbol])
                    case "ETF":
                        res[symbol] = ETFQuote(**res[symbol])
                    case "FUTURE":
                        res[symbol] = FutureQuote(**res[symbol])
                    case "FUTURES_OPTIONS":
                        res[symbol] = FutureOptionsQuote(**res[symbol])
                    case _:
                        pass
            return res
        return {}

    def get_quotes(self, instruments=List[str]) -> dict:
        """Grabs real-time quotes for multiple instruments.

        Overview
        ----
        Serves as the mechanism to make a request to the Get
        Quote and Get Quotes Endpoint. If one item is provided
        a Get Quote request will be made and if more than one
        item is provided then a Get Quotes request will be made.
        Only 500 symbols can be sent at a single time.

        Documentation
        ----
        https://developer.tdameritrade.com/quotes/apis

        Parameters
        ----
        instruments: str
            A list of different financial instruments.

        Usage
        ----
            >>> quote_service = td_client.quotes()
            >>> quote_service.get_quotes(instruments=['AAPL','SQ'])
        """

        params = {"symbol": ",".join(instruments)}

        res = self.session.make_request(
            method="get", endpoint="marketdata/quotes", params=params
        )

        if res:
            # return res
            for symbol in res:
                asset_type = res[symbol]["assetType"]
                match asset_type:
                    case "EQUITY":
                        res[symbol] = EquityQuote(**res[symbol])
                    case "INDEX":
                        res[symbol] = IndexQuote(**res[symbol])
                    case "MUTUAL_FUND":
                        res[symbol] = MutualFundQuote(**res[symbol])
                    case "OPTION":
                        res[symbol] = OptionQuote(**res[symbol])
                    case "FOREX":
                        res[symbol] = ForexQuote(**res[symbol])
                    case "ETF":
                        res[symbol] = ETFQuote(**res[symbol])
                    case "FUTURE":
                        res[symbol] = FutureQuote(**res[symbol])
                    case "FUTURES_OPTIONS":
                        res[symbol] = FutureOptionsQuote(**res[symbol])
                    case _:
                        pass
            return res
        return {}
