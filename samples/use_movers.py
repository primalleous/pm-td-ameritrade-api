from pprint import pprint
from td.client import TdAmeritradeClient
from td.enums.enums import MoversChange, MoversDirection, MoversIndex
from td.models.rest.query import MoversQuery

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

# Initialize the `Movers` service.
movers_service = td_client.movers()

# Grab the top 10 percentage up movers.
pprint(movers_service.get_movers(index="$DJI", direction="up", change="percent"))

pprint(movers_service.get_movers(index="$SPX.X", direction="up", change="percent"))

pprint(
    movers_service.get_movers(index=MoversIndex.COMPX, direction="up", change="percent")
)


movers_query = MoversQuery(
    index=MoversIndex.COMPX, direction=MoversDirection.UP, change=MoversChange.PERCENT
)
pprint(movers_service.get_movers(movers_query))


pprint(
    movers_service.get_movers(
        {
            "index": MoversIndex.COMPX,
            "direction": MoversDirection.UP,
            "change": MoversChange.PERCENT,
        }
    )
)
