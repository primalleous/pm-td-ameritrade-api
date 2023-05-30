from pprint import pprint
from td.client import TdAmeritradeClient
from td.enums.enums import Projections
from td.models.rest.query import InstrumentsQuery

td_client = TdAmeritradeClient()
instruments_service = td_client.instruments()

# Search for a symbol.
pprint(
    instruments_service.search_instruments(symbol="MSFT", projection="symbol-search")
)

# Search for a symbol.
pprint(
    instruments_service.search_instruments(
        {"symbol": "MSFT", "projection": "symbol-search"}
    )
)

instruments_query = InstrumentsQuery(symbol="MSFT", projection="symbol-search")

# Search for a symbol.
pprint(instruments_service.search_instruments(instruments_query))

# Search for fundamental data.
pprint(
    instruments_service.search_instruments(
        symbol="MSFT", projection=Projections.FUNDAMENTAL
    )
)

# Search for a symbol using regular expression.
pprint(
    instruments_service.search_instruments(
        symbol="MS*", projection=Projections.SYMBOL_REGEX
    )
)

# Search for companies using description key words.
pprint(
    instruments_service.search_instruments(
        symbol="Technology", projection=Projections.DESCRIPTION_SEARCH
    )
)

# Search for companies using description key words.
pprint(
    instruments_service.search_instruments(
        symbol="91282CGK1",
        projection=Projections.SYMBOL_SEARCH,
    )
)

# Search for companies using description regular expression.
pprint(
    instruments_service.search_instruments(
        symbol="S&P.*", projection=Projections.DESCRIPTION_REGEX
    )
)


# Get an Insturment by using their CUSIP. Bond
pprint(instruments_service.get_instrument(cusip="91282CGK1"))

# Get an Insturment by using their CUSIP. MSFT
pprint(instruments_service.get_instrument(cusip="594918104"))
