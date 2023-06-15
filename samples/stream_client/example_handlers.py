import logging
from pydantic import ValidationError
from rich import print_json
from td.logger import TdLogger
from td.models.streaming import (
    ActivesData,
    ChartEquityData,
    ChartFuturesOrOptionsData,
    ChartHistorySnapshot,
    LevelOneEquityData,
    LevelOneForexData,
    LevelOneFuturesData,
    LevelOneFuturesOptionsData,
    LevelOneOptionData,
    LevelTwoBookData,
    NewsHeadlineData,
    TimesaleData,
)
from td.streaming.handlers import (
    BaseActivesHandler,
    BaseChartHistoryHandler,
    BaseDataMessageHandler,
)
from td.utils.helpers import get_default_file_path, dict_to_json, save_raw_json


class SymbolDataUpdater(BaseDataMessageHandler):
    """Handles data messages related to symbol data."""

    def __init__(self, model):
        super().__init__(model)
        self.latest_data_by_symbol = {}
        self.latest_message = None
        self.subscribers = {}
        self.log = TdLogger(__name__).logger
        self._log_debug_enabled = self.log.isEnabledFor(logging.DEBUG)

    async def data_message_handler(self, msg):
        try:
            self.latest_message = self.construct_message(msg)
            await self.update_data_by_symbol()
        except ValidationError as e:
            self.log.error(f"Message Construction Error: {e}")
        except Exception as e:
            self.log.error(f"Unknown Error: {e}")

    async def update_data_by_symbol(self):
        latest_data = self.latest_message
        aggregated_data = {}
        symbols = set()
        for data in latest_data.content:
            symbol = data.symbol
            if symbol not in aggregated_data:
                aggregated_data[symbol] = []
            if symbol not in symbols:
                symbols.add(symbol)
            aggregated_data[symbol].append(data)

        for symbol in symbols:
            self.latest_data_by_symbol[symbol] = aggregated_data[symbol]

        for symbol, data_list in aggregated_data.items():
            await self._notify_subscribers(data_list)

        if self._log_debug_enabled:
            await self.handle_debug()

    async def handle_debug(self):
        self.log.debug("\n")
        print_json(self.latest_message.json(exclude_none=True))

    async def subscribe_websocket(self, websocket, symbol):
        if symbol in self.latest_data_by_symbol:
            await websocket.send_json(
                [x.dict() for x in self.latest_data_by_symbol[symbol]]
            )
        if websocket not in self.subscribers:
            self.subscribers[websocket] = set()
        self.subscribers[websocket].add(symbol)

    async def unsubscribe_websocket(self, websocket, symbol):
        if websocket in self.subscribers and symbol in self.subscribers[websocket]:
            self.subscribers[websocket].remove(symbol)
            if len(self.subscribers[websocket]) == 0:
                del self.subscribers[websocket]

    async def _notify_subscribers(self, data_list):
        if self.subscribers:
            for ws, symbols in self.subscribers.items():
                for data in data_list:
                    if data.symbol in symbols:
                        await ws.send_json(data.dict())

    def get_latest_data(self, symbol):
        return self.latest_data_by_symbol.get(symbol, None)


class ActivesHandler(BaseActivesHandler, SymbolDataUpdater):
    async def data_message_handler(self, duration, msg):
        try:
            res = self.construct_message(msg)
            if res:
                latest_data, num_trades_active, num_shares_active = (
                    res[0],
                    res[1],
                    res[2],
                )
                self.latest_message = latest_data

                await self.update_data_by_symbol(
                    duration, num_trades_active, num_shares_active
                )
        except ValidationError as e:
            self.log.error(f"Message Construction Error: {e}")

    async def update_data_by_symbol(
        self, duration, num_trades_active, num_shares_active
    ):
        actives_dict = {
            "num_trades_active": num_trades_active,
            "num_shares_active": num_shares_active,
        }
        for key, data in actives_dict.items():
            if data:
                for symbol_data in data.symbol_data:
                    symbol = symbol_data.symbol
                    self.latest_data_by_symbol[symbol] = {duration: {key: symbol_data}}
        if self._log_debug_enabled:
            await self.handle_debug()

    async def handle_debug(self):
        self.log.debug("\n")
        print_json(self.latest_message.json(exclude_none=True))
        print_json(dict_to_json(self.latest_data_by_symbol))


class TimesaleDataHandler(SymbolDataUpdater):
    pass


class ChartDataHandler(SymbolDataUpdater):
    pass


class BookHandler(SymbolDataUpdater):
    pass


class QuoteHandler(SymbolDataUpdater):
    pass


class NewsHandler(SymbolDataUpdater):
    pass


timesale_handler = TimesaleDataHandler(TimesaleData)

chart_futures_or_options_handler = ChartDataHandler(ChartFuturesOrOptionsData)
chart_equity_handler = ChartDataHandler(ChartEquityData)

book_handler = BookHandler(LevelTwoBookData)

level_one_handler = QuoteHandler(LevelOneEquityData)
level_one_options_handler = QuoteHandler(LevelOneOptionData)
level_one_futures_handler = QuoteHandler(LevelOneFuturesData)
level_one_forex_handler = QuoteHandler(LevelOneForexData)
level_one_futures_options_handler = QuoteHandler(LevelOneFuturesOptionsData)

actives_handler = ActivesHandler(ActivesData)

news_handler = NewsHandler(NewsHeadlineData)


class ChartHistoryFuturesHandler(BaseChartHistoryHandler):
    def __init__(self, model, save_to_directory=False):
        self.model = model
        self.latest_message = None
        self.save_to_directory = save_to_directory
        self.handled_event = None
        self.log = TdLogger(__name__).logger
        self._log_debug_enabled = self.log.isEnabledFor(logging.DEBUG)

    async def snapshot_message_handler(self, handled_event, future, timeframe, msg):
        try:
            self.handled_event = handled_event
            res = self.construct_message(msg)
            if res:
                self.latest_message = res
                if self.save_to_directory:
                    await self.save_raw_msg(future, timeframe, res)
                else:
                    print_json(self.latest_message.json(exclude_none=True))
        except ValidationError as e:
            self.log.error(f"Message Construction Error: {e}")

    async def save_raw_msg(self, future, timeframe, msg):
        """
        Saves to directory specified in config data_paths section.
        Uses calling directory if not specified.
        """
        symbol = msg.content[0].symbol
        if future != symbol:
            raise ValueError(f"future {future} != symbol {symbol}")
        raw_json = {"snapshot": [msg.dict(by_alias=True)]}

        path = get_default_file_path(symbol, timeframe)
        await save_raw_json(raw_json, path)

        self.handled_event.set()

    def raw_message_handler(self, msg):
        """
        Processes a message with the snapshot key {"snapshot":...} and returns pydantic obj representation.
        """
        msg = msg["snapshot"][0]
        return self.construct_message(msg)


chart_history_handler = ChartHistoryFuturesHandler(
    ChartHistorySnapshot, save_to_directory=True
)
