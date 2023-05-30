from datetime import datetime
from td.models.rest.response import OptionChain
from td.session import TdAmeritradeSession
from td.models.rest.query import OptionChainQuery
from td.utils.helpers import QueryInitializer


class OptionsChain:

    """
    ## Overview
    ----
    Allows the user to query options chain data from the
    the TD Ameritrade API along with helping to formulate
    queries.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `OptionsChain` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    @QueryInitializer(OptionChainQuery)
    def get_option_chain(self, option_chain_query: OptionChainQuery) -> OptionChain:
        """Get option chain for an optionable Symbol.

        ### Documentation
        ----
        https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains

        ### Parameters
        ----
        option_chain_query: OptionChainQuery

        ### NOTE: Filters such as ITM/OTM/DTE don't seem to work.

        ### Usage
        ----
            1. Population by field names specified in `OptionChainQuery`
            >>> options_chain_service = td_client.options_chain()
            >>> options_data = options_chain_service.get_option_chain(
                    symbol="SPY",
                    strike_count=1,
                    from_date="2023-05-26T15:03:00",
                    to_date=datetime(2023, 5, 26),
                    option_type=OptionType.ALL,
                    strategy="SINGLE",
                )
            2. Pass a dictionary with field names specified in `OptionChainQuery`
            >>> options_data = options_chain_service.get_option_chain({
                    "symbol": "SPY",
                    "strike_count": 1,
                    "from_date": "2023-05-26T15:03:00",
                    "to_date": datetime(2023, 5, 26),
                    "option_type": "ALL",
                    "strategy": "SINGLE",
                })

            3. Pass an `OptionChainQuery` object directly
            >>> options_chain_query = OptionChainQuery(**{
                    "symbol": "SPY",
                    "strike_count": 1,
                    "from_date": "2023-05-26T15:03:00",
                    "to_date": datetime(2023, 5, 26),
                    "option_type": "ALL",
                    "strategy": "SINGLE",
                })
            >>> options_data = options_chain_service.get_option_chain(options_chain_query)
        """

        res = self.session.make_request(
            method="get",
            endpoint="marketdata/chains",
            params=option_chain_query.dict(by_alias=True),
        )

        if res:
            for option_type in ["putExpDateMap", "callExpDateMap"]:
                if res.get(option_type):
                    new_map = {}
                    for date_key, strike_map in res[option_type].items():
                        # Extract the date part of the key
                        date_str = date_key.split(":")[0]

                        # Verify the date string is formatted correctly
                        try:
                            datetime.strptime(date_str, "%Y-%m-%d")
                        except ValueError:
                            self.log(
                                f"Date parsing error: {date_str} is not a valid date."
                            )
                            continue

                        for strike_price, option_list in strike_map.items():
                            option_symbol = option_list[0]["symbol"]
                            dual_key = f"{date_str},{strike_price},{option_symbol}"

                            new_map[dual_key] = option_list

                    res[option_type] = new_map
            return OptionChain(**res)
