from td.client import TdAmeritradeClient
from td.enums.enums import QOSLevel
from td.config import TdConfiguration
from samples.stream_client.example_handlers import level_one_handler


def callback_func(msg):
    pass
    # print(msg)


config = TdConfiguration()
td_client = TdAmeritradeClient()
stream_client = td_client.streaming_api_client(on_message_received=callback_func)
stream_services = stream_client.services


def run_td_stream_client():
    stream_client.open_stream()  # The running loop argument is removed
    stream_services.quality_of_service(qos_level=QOSLevel.EXPRESS)


def add_quote_handler():
    # level_one_handler is still async but could be written synchronously
    stream_services.add_handler("data", "QUOTE", level_one_handler.data_message_handler)


def main():
    run_td_stream_client()
    add_quote_handler()

    stream_services.level_one_quotes(symbols=["SPY"])

    # Time delay: in synchronous programming, just use sleep from the time module
    import time

    time.sleep(30)


if __name__ == "__main__":
    main()  # asyncio.run is not needed
