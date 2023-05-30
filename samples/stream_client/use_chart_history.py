import asyncio
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import pandas as pd

from td.client import TdAmeritradeClient
from td.enums.enums import ChartFuturesFrequencies, QOSLevel
from td.config import TdConfiguration
from samples.stream_client.example_handlers import (
    ChartHistoryFuturesHandler,
    chart_history_handler,
)
from td.models.streaming import ChartHistorySnapshot


async def callback_func(msg):
    pass
    # print(msg)


config = TdConfiguration()
td_client = TdAmeritradeClient()
stream_client = td_client.streaming_api_client(on_message_received=callback_func)
stream_services = stream_client.services

chart_history_symbol_queue = asyncio.Queue()

try:
    tda_futures_csv_path = Path(config.symbols.tda_futures_path)
except AttributeError:
    tda_futures_csv_path = None
    chart_history_handler = ChartHistoryFuturesHandler(
        ChartHistorySnapshot, save_to_directory=False
    )


async def run_td_stream_client():
    # using the background_thread doesn't work due to sharing an asyncio.Event between threads
    # stream_client.open_stream(asyncio.get_running_loop())

    stream_client.open_stream(asyncio.get_running_loop())
    stream_services.quality_of_service(qos_level=QOSLevel.EXPRESS)


async def bulk_add_to_chart_history_symbol_queue(
    futures_list, timeframe_list, start_date, end_date
):
    for future in futures_list:
        for timeframe in timeframe_list:
            await chart_history_symbol_queue.put(
                (future, timeframe, start_date, end_date)
            )


async def get_futures_data():
    while True:
        future, timeframe, start_date, end_date = await chart_history_symbol_queue.get()

        handled_event = asyncio.Event()

        async def chart_history_handler_func(msg):
            await chart_history_handler.snapshot_message_handler(
                handled_event, future, timeframe, msg
            )

        func_ref = chart_history_handler_func
        stream_services.add_handler("snapshot", "CHART_HISTORY_FUTURES", func_ref)

        print(f"Attempting to pull data for {future}, {timeframe}")
        if timeframe == "minute":
            chart_futures_frequencies = ChartFuturesFrequencies.ONE_MINUTE
        elif timeframe == "daily":
            chart_futures_frequencies = ChartFuturesFrequencies.ONE_DAY
        elif timeframe == "weekly":
            chart_futures_frequencies = ChartFuturesFrequencies.ONE_WEEK
        elif timeframe == "monthly":
            chart_futures_frequencies = ChartFuturesFrequencies.ONE_MONTH

        stream_services.futures_chart_history(
            symbol=[future],
            frequency=chart_futures_frequencies,
            start_time=start_date,
            end_time=end_date,
        )

        print("waiting for event")
        await handled_event.wait()
        print("done waiting for event")

        stream_services.remove_handler("snapshot", "CHART_HISTORY_FUTURES", func_ref)

        print(stream_client.subscribed_services)

        unsubscribe_request_made = False
        continue_requests = False
        while not continue_requests:
            await asyncio.sleep(0.3)
            if not stream_services.is_subscribed("CHART_HISTORY_FUTURES"):
                continue_requests = True
            else:
                if not unsubscribe_request_made:
                    stream_services.futures_unsub_chart_history()
                    unsubscribe_request_made = True
        print(stream_client.subscribed_services)

        if chart_history_symbol_queue.empty():
            break


async def main():
    # The max look back period for futures minute data is 14 days
    end_date = datetime.today() + timedelta(days=1)
    start_date = datetime.now() - timedelta(days=13)

    # daily data for some futures goes back to early 1980s
    # start_date = datetime.strptime("1980-01-01", "%Y-%m-%d")
    # start_date = datetime.now() - timedelta(days=30)

    if tda_futures_csv_path:
        futures_list = pd.read_csv(tda_futures_csv_path)["Symbol"].to_list()
    else:
        futures_list = ["/ES", "/NQ", "/YM", "/RTY"]
    timeframe_list = ["daily", "minute"]

    await run_td_stream_client()
    await bulk_add_to_chart_history_symbol_queue(
        futures_list, timeframe_list, start_date, end_date
    )
    await get_futures_data()

    await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())


# import asyncio, random
#

# async def blah(n):
#     await asyncio.sleep(random.random())
#     results.add(n)

# async def doit(m):
#     for i in range(m):
#         asyncio.create_task(blah(i))
#         await asyncio.sleep(0)
#     await asyncio.sleep(1.01)

# async def main(m):
#     global results
#     results = set()
#     await doit(m)
#     tasks = [t for t in asyncio.all_tasks() if t is not
#         asyncio.current_task()]
#     print(len(tasks))
#     sleep(5)
#     tasks = [t for t in asyncio.all_tasks() if t is not
#             asyncio.current_task()]
#     print(len(tasks))
#     try:
#         print(list(range(m)) == list(results))
#         assert list(range(m)) == list(results)
#     except AssertionError:
#         print(f"For {m} tasks, missing {m - len(results)} results: {set(range(m)) - results}")

# if __name__ == "__main__":
#     asyncio.run(main(10000))
