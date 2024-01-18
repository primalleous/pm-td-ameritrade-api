from typing import List
from pydantic import BaseModel, Field, SerializeAsAny, constr


class BaseStreamingModel(BaseModel):
    class Config:
        populate_by_name = True

    @classmethod
    def get_field_aliases(cls, replace_key=True):
        """Returns aliases in a comma-separated string."""
        temp = [field.alias for field in cls.model_fields.values() if field.alias]
        if replace_key:
            temp = ["0" if alias == "key" else alias for alias in temp]
        return temp


class BaseResponseMessage(BaseStreamingModel):
    service: str
    timestamp: int
    command: str


# data response type


class DataResponseContent(BaseStreamingModel):
    pass


class DataResponseMessage(BaseResponseMessage):
    content: SerializeAsAny[List[DataResponseContent]]


class ExchangeData(BaseStreamingModel):
    exchange: str = Field(alias="0")
    volume: int = Field(alias="1")
    seq: int = Field(alias="2")


class PriceLevelData(BaseStreamingModel):
    price: float = Field(alias="0")
    total_volume: int = Field(alias="1")
    exchange_count: int = Field(alias="2")
    exchanges: SerializeAsAny[List[ExchangeData]] = Field(alias="3")


class LevelTwoBookData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case
    timestamp: int = Field(alias="1")
    bid_data: SerializeAsAny[List[PriceLevelData]] = Field(alias="2")
    ask_data: SerializeAsAny[List[PriceLevelData]] = Field(alias="3")


class LevelOneEquityData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case
    bid_price: float | None = Field(alias="1", default=None)  # Current Best Bid Price
    ask_price: float | None = Field(alias="2", default=None)  # Current Best Ask Price
    last_price: float | None = Field(
        alias="3", default=None
    )  # Price at which the last trade was matched
    bid_size: float | None = Field(alias="4", default=None)  # Number of shares for bid
    ask_size: float | None = Field(alias="5", default=None)  # Number of shares for ask
    ask_id: str | None = Field(alias="6", default=None)  # Exchange with the best ask
    bid_id: str | None = Field(alias="7", default=None)  # Exchange with the best bid
    total_volume: int | None = Field(
        alias="8", default=None
    )  # Aggregated shares traded throughout the day
    last_size: float | None = Field(
        alias="9", default=None
    )  # Number of shares traded with last trade
    trade_time: int | None = Field(
        alias="10", default=None
    )  # Trade time of the last trade in seconds since midnight EST
    quote_time: int | None = Field(
        alias="11", default=None
    )  # Quote time of the last quote in seconds since midnight EST
    high_price: float | None = Field(alias="12", default=None)  # Day’s high trade price
    low_price: float | None = Field(alias="13", default=None)  # Day’s low trade price
    bid_tick: str | None = Field(
        alias="14", default=None
    )  # Indicates Up or Downtick (NASDAQ NMS & Small Cap)
    close_price: float | None = Field(
        alias="15", default=None
    )  # Previous day’s closing price
    exchange_id: str | None = Field(
        alias="16", default=None
    )  # Primary "listing" Exchange
    marginable: bool | None = Field(
        alias="17", default=None
    )  # Stock approved by the Federal Reserve and an investor's broker as being suitable for providing collateral for margin debt.
    shortable: bool | None = Field(alias="18", default=None)  # Stock can be sold short.
    island_bid: float | None = Field(alias="19", default=None)  # No longer used
    island_ask: float | None = Field(alias="20", default=None)  # No longer used
    island_volume: int | None = Field(alias="21", default=None)  # No longer used
    quote_day: int | None = Field(alias="22", default=None)  # Day of the quote
    trade_day: int | None = Field(alias="23", default=None)  # Day of the trade
    volatility: float | None = Field(
        alias="24", default=None
    )  # Option Risk/Volatility Measurement
    description: str | None = Field(
        alias="25", default=None
    )  # A company, index or fund name
    last_id: str | None = Field(
        alias="26", default=None
    )  # Exchange where last trade was executed
    digits: int | None = Field(alias="27", default=None)  # Valid decimal points
    open_price: float | None = Field(alias="28", default=None)  # Day's Open Price
    net_change: float | None = Field(
        alias="29", default=None
    )  # Current Last-Prev Close
    week_52_high: float | None = Field(
        alias="30", default=None
    )  # Highest price traded in the past 52 weeks
    week_52_low: float | None = Field(
        alias="31", default=None
    )  # Lowest price traded in the past 52 weeks
    pe_ratio: float | None = Field(alias="32", default=None)  # N/A
    dividend_amount: float | None = Field(
        alias="33", default=None
    )  # Earnings Per Share
    dividend_yield: float | None = Field(alias="34", default=None)  # Dividend Yield
    island_bid_size: int | None = Field(alias="35", default=None)  # No longer used
    island_ask_size: int | None = Field(alias="36", default=None)  # No longer used
    nav: float | None = Field(alias="37", default=None)  # Mutual Fund Net Asset Value
    fund_price: float | None = Field(alias="38", default=None)  # N/A
    exchange_name: str | None = Field(
        alias="39", default=None
    )  # Display name of exchange
    dividend_date: str | None = Field(alias="40", default=None)  # N/A
    regular_market_quote: bool | None = Field(
        alias="41", default=None
    )  # Is last quote a regular quote
    regular_market_trade: bool | None = Field(
        alias="42", default=None
    )  # Is last trade a regular trade
    regular_market_last_price: float | None = Field(
        alias="43", default=None
    )  # Only records regular trade
    regular_market_last_size: float | None = Field(
        alias="44", default=None
    )  # Currently realize/100, only records regular trade
    regular_market_trade_time: int | None = Field(
        alias="45", default=None
    )  # Only records regular trade
    regular_market_trade_day: int | None = Field(
        alias="46", default=None
    )  # Only records regular trade
    regular_market_net_change: float | None = Field(
        alias="47", default=None
    )  # RegularMarketLastPrice - close
    security_status: str | None = Field(
        alias="48", default=None
    )  # Indicates a symbol's current trading status (Normal, Halted, Closed)
    mark: float | None = Field(alias="49", default=None)  # Mark Price
    quote_time_long: int | None = Field(
        alias="50", default=None
    )  # Last quote time in milliseconds since Epoch
    trade_time_long: int | None = Field(
        alias="51", default=None
    )  # Last trade time in milliseconds since Epoch
    regular_market_trade_time_long: int | None = Field(
        alias="52", default=None
    )  # Regular market trade time in milliseconds since Epoch
    delayed: bool | None = None


class LevelOneOptionData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case
    description: str | None = Field(
        alias="1", default=None
    )  # A company, index or fund name
    bid_price: float | None = Field(alias="2", default=None)  # Current Best Bid Price
    ask_price: float | None = Field(alias="3", default=None)  # Current Best Ask Price
    last_price: float | None = Field(
        alias="4", default=None
    )  # Price at which the last trade was matched
    high_price: float | None = Field(alias="5", default=None)  # Day’s high trade price
    low_price: float | None = Field(alias="6", default=None)  # Day’s low trade price
    close_price: float | None = Field(
        alias="7", default=None
    )  # Previous day’s closing price
    total_volume: int | None = Field(
        alias="8", default=None
    )  # Aggregated shares traded throughout the day, including pre/post market hours.
    open_interest: int | None = Field(alias="9", default=None)
    volatility: float | None = Field(
        alias="10", default=None
    )  # Option Risk/Volatility Measurement
    quote_time: int | None = Field(
        alias="11", default=None
    )  # Trade time of the last quote
    trade_time: int | None = Field(
        alias="12", default=None
    )  # Trade time of the last trade
    money_intrinsic_value: float | None = Field(alias="13", default=None)
    quote_day: int | None = Field(alias="14", default=None)  # Day of the quote
    trade_day: int | None = Field(alias="15", default=None)  # Day of the trade
    expiration_year: int | None = Field(alias="16", default=None)
    multiplier: float | None = Field(alias="17", default=None)
    digits: int | None = Field(alias="18", default=None)  # Valid decimal points
    open_price: float | None = Field(alias="19", default=None)  # Day's Open Price
    bid_size: float | None = Field(alias="20", default=None)  # Number of shares for bid
    ask_size: float | None = Field(alias="21", default=None)  # Number of shares for ask
    last_size: float | None = Field(
        alias="22", default=None
    )  # Number of shares traded with last trade
    net_change: float | None = Field(
        alias="23", default=None
    )  # Current Last-Prev Close
    strike_price: float | None = Field(alias="24", default=None)
    contract_type: str | None = Field(alias="25", default=None)
    underlying: str | None = Field(alias="26", default=None)
    expiration_month: int | None = Field(alias="27", default=None)
    deliverables: str | None = Field(alias="28", default=None)
    time_value: float | None = Field(alias="29", default=None)
    expiration_day: int | None = Field(alias="30", default=None)
    days_to_expiration: int | None = Field(alias="31", default=None)
    delta: float | None = Field(alias="32", default=None)
    gamma: float | None = Field(alias="33", default=None)
    theta: float | None = Field(alias="34", default=None)
    vega: float | None = Field(alias="35", default=None)
    rho: float | None = Field(alias="36", default=None)
    security_status: str | None = Field(
        alias="37", default=None
    )  # Indicates a symbols current trading status, Normal, Halted, Closed
    theoretical_option_value: float | None = Field(alias="38", default=None)
    underlying_price: float | None = Field(alias="39", default=None)
    uv_expiration_type: str | None = Field(alias="40", default=None)
    mark: float | None = Field(alias="41", default=None)  # Mark Price


class LevelOneFuturesData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case.
    bid_price: float | None = Field(alias="1", default=None)  # Current Best Bid Price
    ask_price: float | None = Field(alias="2", default=None)  # Current Best Ask Price
    last_price: float | None = Field(
        alias="3", default=None
    )  # Price at which the last trade was matched
    bid_size: int | None = Field(alias="4", default=None)  # Number of shares for bid
    ask_size: int | None = Field(alias="5", default=None)  # Number of shares for ask
    ask_id: str | None = Field(alias="6", default=None)  # Exchange with the best ask
    bid_id: str | None = Field(alias="7", default=None)  # Exchange with the best bid
    total_volume: float | None = Field(
        alias="8", default=None
    )  # Aggregated shares traded throughout the day, including pre/post market hours
    last_size: int | None = Field(
        alias="9", default=None
    )  # Number of shares traded with last trade
    quote_time: int | None = Field(
        alias="10", default=None
    )  # Trade time of the last quote in milliseconds since epoch
    trade_time: int | None = Field(
        alias="11", default=None
    )  # Trade time of the last trade in milliseconds since epoch
    high_price: float | None = Field(alias="12", default=None)  # Day’s high trade price
    low_price: float | None = Field(alias="13", default=None)  # Day’s low trade price
    close_price: float | None = Field(
        alias="14", default=None
    )  # Previous day’s closing price
    exchange_id: str | None = Field(
        alias="15", default=None
    )  # Primary "listing" Exchange
    description: str | None = Field(
        alias="16", default=None
    )  # Description of the product
    last_id: str | None = Field(
        alias="17", default=None
    )  # Exchange where last trade was executed
    open_price: float | None = Field(alias="18", default=None)  # Day's Open Price
    net_change: float | None = Field(
        alias="19", default=None
    )  # Current Last-Prev Close
    future_percent_change: float | None = Field(
        alias="20", default=None
    )  # Current percent change
    exchange_name: str | None = Field(alias="21", default=None)  # Name of exchange
    security_status: str | None = Field(
        alias="22", default=None
    )  # Trading status of the symbol
    open_interest: int | None = Field(
        alias="23", default=None
    )  # The total number of futures contracts that are not closed or delivered on a particular day
    mark: float | None = Field(
        alias="24", default=None
    )  # Mark-to-Market value is calculated daily using current prices to determine profit/loss
    tick: float | None = Field(alias="25", default=None)  # Minimum price movement
    tick_amount: float | None = Field(
        alias="26", default=None
    )  # Minimum amount that the price of the market can change
    product: str | None = Field(alias="27", default=None)  # Futures product
    future_price_format: str | None = Field(
        alias="28", default=None
    )  # Display in fraction or decimal format
    future_trading_hours: str | None = Field(alias="29", default=None)  # Trading hours
    future_is_tradable: bool | None = Field(
        alias="30", default=None
    )  # Flag to indicate if this future contract is tradable
    future_multiplier: float | None = Field(alias="31", default=None)  # Point value
    future_is_active: bool | None = Field(
        alias="32", default=None
    )  # Indicates if this contract is active
    future_settlement_price: float | None = Field(
        alias="33", default=None
    )  # Closing price
    future_active_symbol: str | None = Field(
        alias="34", default=None
    )  # Symbol of the active contract
    future_expiration_date: int | None = Field(
        alias="35", default=None
    )  # Expiration date of this contract in milliseconds since epoch
    delayed: bool | None = None


class LevelOneForexData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case
    bid_price: float | None = Field(alias="1", default=None)  # Current Best Bid Price
    ask_price: float | None = Field(alias="2", default=None)  # Current Best Ask Price
    last_price: float | None = Field(
        alias="3", default=None
    )  # Price at which the last trade was matched
    bid_size: int | None = Field(alias="4", default=None)  # Number of shares for bid
    ask_size: int | None = Field(alias="5", default=None)  # Number of shares for ask
    total_volume: float | None = Field(
        alias="6", default=None
    )  # Aggregated shares traded throughout the day, including pre/post market hours
    last_size: int | None = Field(
        alias="7", default=None
    )  # Number of shares traded with last trade
    quote_time: int | None = Field(
        alias="8", default=None
    )  # Trade time of the last quote in milliseconds since epoch
    trade_time: int | None = Field(
        alias="9", default=None
    )  # Trade time of the last trade in milliseconds since epoch
    high_price: float | None = Field(alias="10", default=None)  # Day’s high trade price
    low_price: float | None = Field(alias="11", default=None)  # Day’s low trade price
    close_price: float | None = Field(
        alias="12", default=None
    )  # Previous day’s closing price
    exchange_id: str | None = Field(
        alias="13", default=None
    )  # Primary "listing" Exchange
    description: str | None = Field(
        alias="14", default=None
    )  # Description of the product
    open_price: float | None = Field(alias="15", default=None)  # Day's Open Price
    net_change: float | None = Field(
        alias="16", default=None
    )  # Current Last-Prev Close
    percent_change: float | None = Field(
        alias="17", default=None
    )  # Current percent change
    exchange_name: str | None = Field(alias="18", default=None)  # Name of exchange
    digits: int | None = Field(alias="19", default=None)  # Valid decimal points
    security_status: str | None = Field(
        alias="20", default=None
    )  # Trading status of the symbol
    tick: float | None = Field(alias="21", default=None)  # Minimum price movement
    tick_amount: float | None = Field(
        alias="22", default=None
    )  # Minimum amount that the price of the market can change
    product: str | None = Field(alias="23", default=None)  # Product name
    trading_hours: str | None = Field(alias="24", default=None)  # Trading hours
    is_tradable: bool | None = Field(
        alias="25", default=None
    )  # Flag to indicate if this forex is tradable
    market_maker: str | None = Field(alias="26", default=None)
    week_52_high: float | None = Field(
        alias="27", default=None
    )  # Highest price traded in the past 12 months, or 52 weeks
    week_52_low: float | None = Field(
        alias="28", default=None
    )  # Lowest price traded in the past 12 months, or 52 weeks
    mark: float | None = Field(
        alias="29", default=None
    )  # Mark-to-Market value is calculated daily using current prices to determine profit/loss
    delayed: bool | None = None


# TODO: mark doesn't match up with spec, it's the contract where it should be a price, maybe other errors too
class LevelOneFuturesOptionsData(DataResponseContent):
    symbol: str = Field(alias="key")  # Ticker symbol in upper case
    bid_price: float | None = Field(alias="1", default=None)  # Current Best Bid Price
    ask_price: float | None = Field(alias="2", default=None)  # Current Best Ask Price
    last_price: float | None = Field(
        alias="3", default=None
    )  # Price at which the last trade was matched
    bid_size: int | None = Field(alias="4", default=None)  # Number of shares for bid
    ask_size: int | None = Field(alias="5", default=None)  # Number of shares for ask
    ask_id: str | None = Field(alias="6", default=None)  # Exchange with the best ask
    bid_id: str | None = Field(alias="7", default=None)  # Exchange with the best bid
    total_volume: float | None = Field(
        alias="8", default=None
    )  # Aggregated shares traded throughout the day, including pre/post market hours
    last_size: int | None = Field(
        alias="9", default=None
    )  # Number of shares traded with last trade
    quote_time: int | None = Field(
        alias="10", default=None
    )  # Trade time of the last quote in milliseconds since epoch
    trade_time: int | None = Field(
        alias="11", default=None
    )  # Trade time of the last trade in milliseconds since epoch
    high_price: float | None = Field(alias="12", default=None)  # Day’s high trade price
    low_price: float | None = Field(alias="13", default=None)  # Day’s low trade price
    close_price: float | None = Field(
        alias="14", default=None
    )  # Previous day’s closing price
    exchange_id: str | None = Field(
        alias="15", default=None
    )  # Primary "listing" Exchange, I = ICE, E = CME, L=LIFFEUS
    description: str | None = Field(
        alias="16", default=None
    )  # Description of the product
    last_id: str | None = Field(
        alias="17", default=None
    )  # Exchange where last trade was executed
    open_price: float | None = Field(alias="18", default=None)  # Day's Open Price
    net_change: float | None = Field(
        alias="19", default=None
    )  # Current Last-Prev Close,  If(close>0) change = last – close else change=0
    future_percent_change: float | None = Field(
        alias="20", default=None
    )  # Current percent change If(close>0) pctChange = (last – close)/close else pctChange=0
    exchange_name: str | None = Field(alias="21", default=None)  # Name of exchange
    security_status: str | None = Field(
        alias="22", default=None
    )  # Trading status of the symbol, Indicates a symbols current trading status, Normal, Halted, Closed
    open_interest: int | None = Field(
        alias="23", default=None
    )  # The total number of futures contracts that are not closed or delivered on a particular day
    contract: str | None = Field(alias="24", default=None)
    tick: float | None = Field(
        alias="25", default=None
    )  # Minimum price movement, From Database (priceIncrement)
    tick_amount: float | None = Field(
        alias="26", default=None
    )  # Minimum amount that the price of the market can change, Tick * multiplier field from database
    mark: str | None = Field(alias="27", default=None)  # TODO: is contract not price
    future_price_format: str | None = Field(
        alias="28", default=None
    )  # Display in fraction or decimal format
    future_trading_hours: str | None = Field(alias="29", default=None)  # Trading hours
    future_is_tradable: bool | None = Field(
        alias="30", default=None
    )  # Flag to indicate if this future contract is tradable
    future_multiplier: float | None = Field(alias="31", default=None)  # Point value
    future_is_active: bool | None = Field(
        alias="32", default=None
    )  # Indicates if this contract is active
    future_settlement_price: float | None = Field(
        alias="33", default=None
    )  # Closing price
    future_active_symbol: str | None = Field(
        alias="34", default=None
    )  # Symbol of the active contract
    future_expiration_date: int | None = Field(
        alias="35", default=None
    )  # Expiration date of this contract in milliseconds since epoch
    delayed: bool | None = None


class NewsHeadlineData(DataResponseContent):
    symbol: str = Field(alias="key")  # Symbol
    error_code: int | None = Field(alias="1", default=None)  # Error Code
    timestamp: int | None = Field(alias="2", default=None)  # Story Datetime
    headline_id: str | None = Field(alias="3", default=None)  # Headline ID
    status: str | None = Field(alias="4", default=None)  # Status
    headline: str | None = Field(alias="5", default=None)  # Headline
    story_id: str | None = Field(alias="6", default=None)  # Story ID
    keyword_count: int | None = Field(alias="7", default=None)  # Count for Keyword
    keyword_array: str | None = Field(alias="8", default=None)  # Keyword Array
    is_hot: bool | None = Field(alias="9", default=None)  # Is Hot
    story_source: str | None = Field(alias="10", default=None)  # Story Source
    seq: int | None = None


class TimesaleData(DataResponseContent):
    symbol: str = Field(alias="key")  # Symbol
    timestamp: int | None = Field(alias="1", default=None)  # Trade Time
    price: float | None = Field(alias="2", default=None)  # Last Price
    volume: int | None = Field(alias="3", default=None)  # Volume
    bid_size: int | None = Field(alias="4", default=None)  # Last Size
    seq: int | None = None


class ChartData(DataResponseContent):
    symbol: str = Field(alias="key")


class ChartEquityData(ChartData):
    open: float | None = Field(alias="1", default=None)
    high: float | None = Field(alias="2", default=None)
    low: float | None = Field(alias="3", default=None)
    close: float | None = Field(alias="4", default=None)
    volume: int | None = Field(alias="5", default=None)
    seq: int | None = Field(alias="6", default=None)
    timestamp: int | None = Field(alias="7", default=None)
    chart_day: int | None = Field(alias="8", default=None)


class ChartFuturesOrOptionsData(ChartData):
    timestamp: int | None = Field(alias="1", default=None)
    open: float | None = Field(alias="2", default=None)
    high: float | None = Field(alias="3", default=None)
    low: float | None = Field(alias="4", default=None)
    close: float | None = Field(alias="5", default=None)
    volume: int | None = Field(alias="6", default=None)
    seq: int | None = None


class ActivesSymbol(BaseStreamingModel):
    symbol: str
    volume: int
    percent: float  # volume / total volume where Total volume (or total # of trades) for the exchange


class ActivesGroup(BaseStreamingModel):
    group_number: str
    num_entries: str
    total_volume: int
    symbol_data: SerializeAsAny[List[ActivesSymbol]]


class ActivesDataGroup(BaseStreamingModel):
    group_id: str
    sample_duration: int
    start_time: constr(
        pattern=r"((0?[1-9]|1[0-2]):[0-5]?\d:[0-5]?\d)|((1[3-9]|2[0-3]):[0-5]?\d:[0-5]?\d)"
    )
    display_time: constr(
        pattern=r"((0?[1-9]|1[0-2]):[0-5]?\d:[0-5]?\d)|((1[3-9]|2[0-3]):[0-5]?\d:[0-5]?\d)"
    )
    num_groups: int
    num_trades_active: ActivesGroup | None = None
    num_shares_active: ActivesGroup | None = None


class ActivesData(DataResponseContent):
    key: str
    actives_data: ActivesDataGroup = Field(alias="1")


# snapshot response type


class SnapshotResponseContent(BaseStreamingModel):
    pass


class SnapshotResponseMessage(BaseResponseMessage):
    content: SerializeAsAny[List[SnapshotResponseContent]]


class ChartHistorySnapshotData(SnapshotResponseContent):
    timestamp: int = Field(alias="0")
    open: float = Field(alias="1")
    high: float = Field(alias="2")
    low: float = Field(alias="3")
    close: float = Field(alias="4")
    volume: float = Field(alias="5")


class ChartHistorySnapshot(SnapshotResponseContent):
    symbol: str = Field(alias="key")
    request_id: str = Field(alias="0")
    unknown_1: str | int = Field(alias="1")
    unknown_2: str | int = Field(alias="2")
    data: SerializeAsAny[List[ChartHistorySnapshotData]] = Field(alias="3")
