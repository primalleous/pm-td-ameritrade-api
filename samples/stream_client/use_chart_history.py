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
    tda_futures_csv_path = Path(config.symbols.tda_future_symbols_path)
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

        try:
            await asyncio.wait_for(handled_event.wait(), timeout=15)
        except asyncio.TimeoutError:
            print(
                f"Timeout occurred while waiting for {future} {timeframe} {start_date} {end_date}"
            )

        stream_services.remove_handler("snapshot", "CHART_HISTORY_FUTURES", func_ref)
        stream_services.futures_unsub_chart_history()

        continue_requests = False
        unsubscribed = False
        handler_removed = False
        while not continue_requests:
            await asyncio.sleep(0.3)
            if not stream_services.is_subscribed("CHART_HISTORY_FUTURES"):
                unsubscribed = True
            if not stream_services.has_handler(
                "snapshot", "CHART_HISTORY_FUTURES", func_ref
            ):
                handler_removed = True
            if handler_removed and unsubscribed:
                continue_requests = True

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
