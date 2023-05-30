# does not actually return data, bid and ask are blank

import asyncio
from datetime import datetime, timedelta

from td.client import TdAmeritradeClient
from td.enums.enums import QOSLevel
from td.config import TdConfiguration
from td.orders.options import OptionSymbol
from samples.stream_client.example_handlers import book_handler


async def callback_func(msg):
    pass
    # print(msg)


config = TdConfiguration()
td_client = TdAmeritradeClient()
stream_client = td_client.streaming_api_client(on_message_received=callback_func)
stream_services = stream_client.services


async def run_td_stream_client():
    stream_client.open_stream(asyncio.get_running_loop())
    stream_services.quality_of_service(qos_level=QOSLevel.EXPRESS)


async def add_book_handler():
    stream_services.add_handler(
        "data", "OPTIONS_BOOK", book_handler.data_message_handler
    )


today = datetime.now() + timedelta(days=1)
today = datetime.now()

month_day_year = today.strftime("%m%d%y")

option_symbol = OptionSymbol("SPY", month_day_year, "C", "420").build()


async def main():
    await run_td_stream_client()
    await add_book_handler()

    stream_services.level_two_options(symbols=[option_symbol])

    await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
