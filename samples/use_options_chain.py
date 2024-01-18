from datetime import datetime

from rich import print_json

from td.client import TdAmeritradeClient
from td.enums.enums import OptionType
from td.models.rest.query import OptionChainQuery

td_client = TdAmeritradeClient()

options_chain_service = td_client.options_chain()

options_data = options_chain_service.get_option_chain(
    symbol="SPY",
    strike_count=1,
    from_date="2024-01-16T15:03:00",
    to_date=datetime(2024, 1, 17),
    option_type=OptionType.ALL,
    strategy="SINGLE",
)

print_json(options_data.model_dump_json())

options_data = options_chain_service.get_option_chain(
    {
        "symbol": "SPY",
        "strike_count": 1,
        "from_date": datetime.now(),
        "to_date": datetime.now(),
        "option_type": "ALL",
        "strategy": "SINGLE",
    }
)

print_json(options_data.model_dump_json())

options_chain_query = OptionChainQuery(
    **{
        "symbol": "SPY",
        "strike_count": 1,
        "from_date": "2024-01-16T15:03:00",
        "to_date": "2024-01-18",
        "option_type": "ALL",
        "strategy": "SINGLE",
    }
)

options_data = options_chain_service.get_option_chain(options_chain_query)

print_json(options_data.model_dump_json())
