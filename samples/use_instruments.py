from rich import print as rprint

from td.client import TdAmeritradeClient
from td.enums.enums import Projections
from td.models.rest.query import InstrumentsQuery

td_client = TdAmeritradeClient()
instruments_service = td_client.instruments()

# Search for a symbol.
rprint(
    instruments_service.search_instruments(symbol="MSFT", projection="symbol-search")
)

# Search for a symbol.
rprint(
    instruments_service.search_instruments(
        {"symbol": "MSFT", "projection": "symbol-search"}
    )
)

instruments_query = InstrumentsQuery(symbol="MSFT", projection="symbol-search")

# Search for a symbol.
rprint(instruments_service.search_instruments(instruments_query))

# Search for fundamental data.
rprint(
    instruments_service.search_instruments(
        symbol="MSFT", projection=Projections.FUNDAMENTAL
    )
)

# Search for a symbol using regular expression.
rprint(
    instruments_service.search_instruments(
        symbol="MS*", projection=Projections.SYMBOL_REGEX
    )
)

# Search for companies using description key words.
rprint(
    instruments_service.search_instruments(
        symbol="Technology", projection=Projections.DESCRIPTION_SEARCH
    )
)

# Search for companies using description key words.
rprint(
    instruments_service.search_instruments(
        symbol="91282CGK1",
        projection=Projections.SYMBOL_SEARCH,
    )
)

# Search for companies using description regular expression.
rprint(
    instruments_service.search_instruments(
        symbol="S&P.*", projection=Projections.DESCRIPTION_REGEX
    )
)


# Get an Insturment by using their CUSIP. Bond
rprint(instruments_service.get_instrument(cusip="91282CGK1"))

# Get an Insturment by using their CUSIP. MSFT
rprint(instruments_service.get_instrument(cusip="594918104"))
