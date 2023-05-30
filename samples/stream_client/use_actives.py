import asyncio

from td.client import TdAmeritradeClient
from td.enums.enums import ActivesDurations, ActivesServices, ActivesVenues, QOSLevel
from td.config import TdConfiguration
from samples.stream_client.example_handlers import actives_handler


async def callback_func(msg):
    # pass
    print(msg)


config = TdConfiguration()
td_client = TdAmeritradeClient()
stream_client = td_client.streaming_api_client(on_message_received=callback_func)
stream_services = stream_client.services


async def run_td_stream_client():
    stream_client.open_stream(asyncio.get_running_loop())
    stream_services.quality_of_service(qos_level=QOSLevel.EXPRESS)


async def add_actives_handler():
    # pass
    stream_services.add_handler(
        "data",
        "ACTIVES_NYSE",
        lambda msg: actives_handler.data_message_handler(duration, msg),
    )


async def main():
    global duration
    duration = ActivesDurations.ALL.value
    await run_td_stream_client()
    await add_actives_handler()

    stream_services.actives(
        ActivesServices.ACTIVES_NYSE, ActivesVenues.NEW_YORK_STOCK_EXCHANGE, duration
    )

    await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
