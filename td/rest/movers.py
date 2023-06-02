from typing import List
from td.models.rest.query import MoversQuery
from td.models.rest.response import Mover
from td.session import TdAmeritradeSession
from td.utils.helpers import QueryInitializer


class Movers:

    """
    ## Overview
    ----
    Allows the user to query the top movers for the
    different indexes based on the type of move.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Movers` services.

        Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    @QueryInitializer(MoversQuery)
    def get_movers(self, movers_query: MoversQuery) -> List[Mover]:
        """Gets Active movers for a specific Index.

        Overview
        ----
        Top 10 (up or down) movers by value or percent for
        a particular market.

        Documentation
        ----
        https://developer.tdameritrade.com/movers/apis/get/marketdata

        Parameters
        ----
        movers_query : MoversQuery

        Usage
        ----
            1. Population by field names specified in `MoversQuery`
            >>> movers_service = td_client.movers()
            >>> movers = movers_service.get_movers(
                    index="$DJI",
                    direction="up",
                    change="percent"
                )
            2. Pass a dictionary with field names specified in `MoversQuery`
            >>> movers = movers_service.get_movers({
                    "index": MoversIndex.COMPX,
                    "direction": MoversDirection.UP,
                    "change": MoversChange.PERCENT,
                })

            3. Pass an `MoversQuery` object directly
            >>> movers_query = MoversQuery(
                    index=MoversIndex.COMPX,
                    direction=MoversDirection.UP,
                    change=MoversChange.PERCENT
                )
                movers = movers_service.get_movers(movers_query)
        """

        res = self.session.make_request(
            method="get",
            endpoint=f"marketdata/{movers_query.index}/movers",
            params=movers_query.dict(by_alias=True),
        )

        if res:
            return [Mover(**mover) for mover in res]
        else:
            return []
