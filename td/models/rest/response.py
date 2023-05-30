from typing import Dict, List
from pydantic import Field
from td.enums.enums import ACHStatus, ResponseTransactionType
from td.models.base_api_model import BaseApiModel
from td.models.orders import BaseInstrument, Order

# TODO
# Authentication - Delay for now
# User Info and Preferences - Delay for now
# Saved Orders - Might not do since Schwab integration is removing functionality
# Watchlist - Might not do since Schwab integration is removing functionality


class BaseResponseModel(BaseApiModel):
    pass


# Instruments


class Fundamental(BaseResponseModel):
    beta: float
    book_value_per_share: float
    current_ratio: float
    div_growth_rate_3_year: float
    dividend_amount: float
    dividend_date: str
    dividend_pay_amount: float
    dividend_pay_date: str
    dividend_yield: float
    eps_change: float
    eps_change_percent_TTM: float
    eps_change_year: float
    eps_TTM: float
    gross_margin_MRQ: float
    gross_margin_TTM: float
    high52: float
    interest_coverage: float
    low52: float
    lt_debt_to_equity: float
    market_cap: float
    market_cap_float: float
    net_profit_margin_MRQ: float
    net_profit_margin_TTM: float
    operating_margin_MRQ: float
    operating_margin_TTM: float
    pb_ratio: float
    pcf_ratio: float
    pe_ratio: float
    peg_ratio: float
    pr_ratio: float
    quick_ratio: float
    return_on_assets: float
    return_on_equity: float
    return_on_investment: float
    rev_change_in: float
    rev_change_TTM: float
    rev_change_year: float
    shares_outstanding: float
    short_int_day_to_cover: float
    short_int_to_float: float
    symbol: str
    total_debt_to_capital: float
    total_debt_to_equity: float
    vol_10_day_avg: float
    vol_1_day_avg: float
    vol_3_month_avg: float


class InstrumentFundamental(BaseInstrument):
    fundamental: Fundamental


class BondInstrument(BaseInstrument):
    bond_factor: float | None
    bond_price: float


# Market Hours


class BaseSession(BaseResponseModel):
    end: str
    start: str


class SessionHours(BaseResponseModel):
    post_market: List[BaseSession] | None
    pre_market: List[BaseSession] | None
    regular_market: List[BaseSession] | None


class MarketHoursResponse(BaseResponseModel):
    category: str | None
    date: str
    exchange: str | None
    is_open: bool
    market_type: str
    product: str
    product_name: str | None
    session_hours: SessionHours | None


# Movers


class Mover(BaseResponseModel):
    change: float
    description: str
    direction: str
    last: float
    symbol: str
    total_volume: int


# Option Chains


class OptionDeliverable(BaseResponseModel):
    symbol: str
    asset_type: str
    deliverable_units: str
    currency_type: str


class OptionQuote(BaseResponseModel):
    put_call: str
    symbol: str
    description: str
    exchange_name: str
    bid: float
    ask: float
    last: float
    mark: float
    bid_size: int
    ask_size: int
    bid_ask_size: str
    last_size: int
    high_price: float
    low_price: float
    open_price: float | None
    close_price: float
    total_volume: int
    trade_date: str | None
    trade_time: int = Field(alias="tradeTimeInLong")
    quote_time_in_long: int = Field(alias="quoteTimeInLong")
    net_change: float
    volatility: float
    delta: float | None
    gamma: float | None
    theta: float | None
    vega: float | None
    rho: float | None
    open_interest: int
    time_value: float
    theoretical_option_value: float
    theoretical_volatility: float
    option_deliverables: List[OptionDeliverable] | None
    strike_price: float
    expiration_date: int
    days_to_expiration: int
    expiration_type: str
    last_trading_day: int
    multiplier: float
    settlement_type: str
    deliverable_note: str
    is_index_option: bool | None
    percent_change: float
    mark_change: float
    mark_percent_change: float
    intrinsic_value: float
    non_standard: bool
    in_the_money: bool
    mini: bool
    penny_pilot: bool


class ExpDateMap(BaseResponseModel):
    __root__: Dict[str, List[OptionQuote]]


class OptionUnderlying(BaseResponseModel):
    ask: float
    ask_size: int
    bid: float
    bid_size: int
    change: float
    close: float
    delayed: bool
    description: str
    exchange_name: str
    fifty_two_week_high: float
    fifty_two_week_low: float
    high_price: float
    last: float
    low_price: float
    mark: float
    mark_change: float
    mark_percent_change: float
    open_price: float
    percent_change: float
    quote_time: int
    symbol: str
    total_volume: int
    trade_time: int


class OptionChain(BaseResponseModel):
    symbol: str
    status: str
    strategy: str
    interval: float
    is_delayed: bool
    is_index: bool
    interest_rate: float
    volatility: float
    days_to_expiration: float
    number_of_contracts: int
    call_exp_date_map: ExpDateMap | None
    put_exp_date_map: ExpDateMap | None
    underlying: OptionUnderlying | None
    underlying_price: float | None


# Price History


class Candle(BaseResponseModel):
    close: float
    datetime: int
    high: float
    low: float
    open: float
    volume: int


class PriceHistoryResponse(BaseResponseModel):
    candles: List[Candle] | None
    empty: bool
    symbol: str


# Quotes


class BaseQuotes(BaseResponseModel):
    symbol: str
    description: str
    exchange: str
    exchange_name: str
    security_status: str


class MutualFundQuote(BaseQuotes):
    close_price: float
    net_change: float
    total_volume: int
    trade_time: int = Field(alias="tradeTimeInLong")
    digits: int
    high_52wk: float = Field(alias="52WkHigh")
    low_52wk: float = Field(alias="52WkHigh")
    nAV: float
    pe_ratio: float
    div_amount: float
    div_yield: float
    div_date: str


class FutureQuote(BaseQuotes):
    bid_price: float = Field(alias="bidPriceInDouble")
    ask_price: float = Field(alias="askPriceInDouble")
    last_price: float = Field(alias="lastPriceInDouble")
    bid_id: str
    ask_id: str
    high_price: float = Field(alias="highPriceInDouble")
    low_price: float = Field(alias="lowPriceInDouble")
    close_price: float = Field(alias="closePriceInDouble")
    last_id: str
    open_price: float = Field(alias="openPriceInDouble")
    change: float = Field(alias="changeInDouble")
    future_percent_change: float
    open_interest: int
    mark: float
    tick: float
    tick_amount: float
    product: str
    future_price_format: str
    future_trading_hours: str
    future_is_tradable: bool
    future_multiplier: int
    future_is_active: bool
    future_settlement_price: float
    future_active_symbol: str
    future_expiration_date: str


class FutureOptionsQuote(BaseQuotes):
    bid_price: float = Field(alias="bidPriceInDouble")
    ask_price: float = Field(alias="askPriceInDouble")
    last_price: float = Field(alias="lastPriceInDouble")
    high_price: float = Field(alias="highPriceInDouble")
    low_price: float = Field(alias="lowPriceInDouble")
    close_price: float = Field(alias="closePriceInDouble")
    open_price: float = Field(alias="openPriceInDouble")
    net_change: float = Field(alias="netChangeInDouble")
    open_interest: int
    volatility: float
    money_intrinsic_value: float = Field(alias="moneyIntrinsicValueInDouble")
    multiplier: float = Field(alias="multiplierInDouble")
    digits: int
    strike_price: float = Field(alias="strikePriceInDouble")
    contract_type: str
    underlying: str
    time_value: float = Field(alias="timeValueInDouble")
    delta: float = Field(alias="deltaInDouble")
    gamma: float = Field(alias="gammaInDouble")
    theta: float = Field(alias="thetaInDouble")
    vega: float = Field(alias="vegaInDouble")
    rho: float = Field(alias="rhoInDouble")
    mark: float
    tick: float
    tick_amount: float
    future_is_tradable: bool
    future_trading_hours: str
    future_percent_change: float
    future_is_active: bool
    future_expiration_date: int
    expiration_type: str
    exercise_type: str
    in_the_money: bool


class IndexQuote(BaseQuotes):
    last_price: float
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    net_change: float
    total_volume: int
    trade_time: int = Field(alias="tradeTimeInLong")
    digits: int
    high_52wk: float = Field(alias="52WkHigh")
    low_52wk: float = Field(alias="52WkHigh")


class OptionQuote(BaseQuotes):
    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    last_price: float
    last_size: int
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    net_change: float
    total_volume: int
    quote_time_in_long: int = Field(alias="quoteTimeInLong")
    trade_time: int = Field(alias="tradeTimeInLong")
    mark: float
    open_interest: int
    volatility: float
    money_intrinsic_value: float
    multiplier: int
    strike_price: float
    contract_type: str
    underlying: str
    time_value: float
    deliverables: str
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    theoretical_option_value: float
    underlying_price: float
    uv_expiration_type: str
    settlement_type: str


class ForexQuote(BaseQuotes):
    bid_price: float = Field(alias="bidPriceInDouble")
    ask_price: float = Field(alias="askPriceInDouble")
    last_price: float = Field(alias="lastPriceInDouble")
    high_price: float = Field(alias="highPriceInDouble")
    low_price: float = Field(alias="lowPriceInDouble")
    close_price: float = Field(alias="closePriceInDouble")
    open_price: float = Field(alias="openPriceInDouble")
    change: float = Field(alias="changeInDouble")
    percent_change: float
    digits: int
    tick: float
    tick_amount: float
    product: str
    trading_hours: str
    is_tradable: bool
    market_maker: str
    high_52wk: float = Field(alias="52WkHighInDouble")
    low_52wk: float = Field(alias="52WkLowInDouble")
    mark: float


class ETFQuote(BaseQuotes):
    bid_price: float
    bid_size: int
    bid_id: str
    ask_price: float
    ask_size: int
    ask_id: str
    last_price: float
    last_size: int
    last_id: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    net_change: float
    total_volume: int
    quote_time_in_long: int = Field(alias="quoteTimeInLong")
    trade_time: int = Field(alias="tradeTimeInLong")
    mark: float
    marginable: bool
    shortable: bool
    volatility: float
    digits: int
    high_52wk: float = Field(alias="52WkHigh")
    low_52wk: float = Field(alias="52WkHigh")
    pe_ratio: float
    div_amount: float
    div_yield: float
    div_date: str
    regular_market_last_price: float
    regular_market_last_size: int
    regular_market_net_change: float
    regular_market_trade_time: int = Field(alias="regularMarketTradeTimeInLong")


class EquityQuote(BaseQuotes):
    bid_price: float
    bid_size: int
    bid_id: str
    ask_price: float
    ask_size: int
    ask_id: str
    last_price: float
    last_size: int
    last_id: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    net_change: float
    total_volume: int
    quote_time_in_long: int = Field(alias="quoteTimeInLong")
    trade_time: int = Field(alias="tradeTimeInLong")
    mark: float
    marginable: bool
    shortable: bool
    volatility: float
    digits: int
    high_52wk: float = Field(alias="52WkHigh")
    low_52wk: float = Field(alias="52WkHigh")
    pe_ratio: float
    div_amount: float
    div_yield: float
    div_date: str
    regular_market_last_price: float
    regular_market_last_size: int
    regular_market_net_change: float
    regular_market_trade_time: int = Field(alias="regularMarketTradeTimeInLong")


# Accounts and Trading (Orders)


class AccountPositions(BaseResponseModel):
    average_price: float
    current_day_cost: float
    current_day_profit_loss: float
    current_day_profit_loss_percentage: float
    instrument: BaseInstrument
    long_quantity: float
    maintenance_requirement: float
    market_value: float
    previous_session_long_quantity: float
    settled_long_quantity: float
    settled_short_quantity: float
    short_quantity: float


# class AccountOrderStrategies(BaseResponseModel):
#     pass


class AccountInitialBalances(BaseResponseModel):
    account_value: float | None = None
    accrued_interest: float | None = None
    cash_available_for_trading: float | None = None
    bond_value: float | None = None
    cash_balance: float | None = None
    cash_receipts: float | None = None
    is_in_call: bool | None = None
    liquidation_value: float | None = None
    long_option_market_value: float | None = None
    long_stock_value: float | None = None
    money_market_fund: float | None = None
    mutual_fund_value: float | None = None
    pending_deposits: float | None = None
    short_option_market_value: float | None = None
    short_stock_value: float | None = None
    available_funds_non_marginable_trade: float | None = (
        None  # The following fields are exclusive to MarginAccount
    )
    buying_power: float | None = None
    day_trading_buying_power: float | None = None
    day_trading_buying_power_call: float | None = None
    day_trading_equity_call: float | None = None
    equity: float | None = None
    equity_percentage: float | None = None
    long_margin_value: float | None = None
    maintenance_call: float | None = None
    maintenance_requirement: float | None = None
    margin: float | None = None
    margin_balance: float | None = None
    margin_equity: float | None = None
    short_margin_value: float | None = None
    total_cash: float | None = None
    cash_available_for_withdrawal: float | None = (
        None  # The following fields are exclusive to CashAccount
    )
    cash_debit_call_value: float | None = None
    unsettled_cash: float | None = None


class AccountCurrentBalances(BaseResponseModel):
    accrued_interest: float  # Fields in MarginAccount & CashAccount ordered by elements in MarginAccount first
    cash_balance: float
    cash_receipts: float
    bond_value: float
    liquidation_value: float
    long_market_value: float
    long_option_market_value: float
    money_market_fund: float
    mutual_fund_value: float
    pending_deposits: float
    savings: float
    short_market_value: float
    short_option_market_value: float
    available_funds: float | None = (
        None  # Fields in MarginAccount but not in CashAccount
    )
    available_funds_non_marginable_trade: float | None = None
    buying_power: float | None = None
    buying_power_non_marginable_trade: float | None = None
    day_trading_buying_power: float | None = None
    equity: float | None = None
    equity_percentage: float | None = None
    long_margin_value: float | None = None
    maintenance_call: float | None = None
    maintenance_requirement: float | None = None
    margin_balance: float | None = None
    reg_t_call: float | None = None
    short_balance: float | None = None
    short_margin_value: float | None = None
    sma: float | None = None
    cash_available_for_trading: float | None = (
        None  # Fields in CashAccount but not in MarginAccount
    )
    cash_available_for_withdrawal: float | None = None
    cash_call: float | None = None
    cash_debit_call_value: float | None = None
    long_non_marginable_market_value: float | None = None
    total_cash: float | None = None
    unsettled_cash: float | None = None


class AccountProjectedBalances(BaseResponseModel):
    accrued_interest: float | None = None  # present in both
    cash_balance: float | None = None
    cash_receipts: float | None = None
    long_option_market_value: float | None = None
    liquidation_value: float | None = None
    long_market_value: float | None = None
    money_market_fund: float | None = None
    savings: float | None = None
    short_market_value: float | None = None
    pending_deposits: float | None = None
    short_option_market_value: float | None = None
    mutual_fund_value: float | None = None
    bond_value: float | None = None
    available_funds: float | None = None  # only present in MarginAccount
    available_funds_non_marginable_trade: float | None = None
    buying_power: float | None = None
    buying_power_non_marginable_trade: float | None = None
    day_trading_buying_power: float | None = None
    day_trading_buying_power_call: float | None = None
    equity: float | None = None
    equity_percentage: float | None = None
    long_margin_value: float | None = None
    maintenance_call: float | None = None
    maintenance_requirement: float | None = None
    margin_balance: float | None = None
    reg_t_call: float | None = None
    short_balance: float | None = None
    short_margin_value: float | None = None
    sma: float | None = None
    is_in_call: bool | None = None
    stock_buying_power: float | None = None
    option_buying_power: float | None = None
    cash_available_for_trading: float | None = None  # only present in CashAccount
    cash_available_for_withdrawal: float | None = None
    cash_call: float | None = None
    long_non_marginable_market_value: float | None = None
    total_cash: float | None = None
    cash_debit_call_value: float | None = None
    unsettled_cash: float | None = None


class SecuritiesAccount(BaseResponseModel):
    account_id: str
    type_: str = Field(alias="type")
    round_trips: int
    is_day_trader: bool
    is_closing_only_restricted: bool
    positions: List[AccountPositions] | None
    order_strategies: List[Order] | None
    initial_balances: AccountInitialBalances | None
    current_balances: AccountCurrentBalances | None
    projected_balances: AccountProjectedBalances | None


# Transactions


class Fees(BaseResponseModel):
    additional_fee: float
    cdsc_fee: float
    commission: float
    opt_reg_fee: float
    other_charges: float
    r_fee: float
    reg_fee: float
    sec_fee: float


class TransactionInstrument(BaseResponseModel):
    symbol: str | None
    underlying_symbol: str | None
    option_expiration_date: str | None
    option_strike_price: float | None
    put_call: str | None
    cusip: str
    description: str | None
    asset_type: str
    bond_maturity_date: str | None
    bond_interest_rate: float | None


class TransactionItem(BaseResponseModel):
    account_id: int
    amount: float | None
    price: float | None
    cost: float
    parent_order_key: int | None
    parent_child_indicator: str | None
    instruction: str | None
    position_effect: str | None
    instrument: TransactionInstrument | None


class Transaction(BaseResponseModel):
    type_: ResponseTransactionType = Field(alias="type")
    clearing_reference_number: str | None
    sub_account: str
    settlement_date: str
    order_id: str | None
    sma: float | None
    requirement_reallocation_amount: float | None
    day_trade_buying_power_effect: float | None
    net_amount: float
    transaction_date: str
    order_date: str | None
    transaction_sub_type: str
    transaction_id: int
    cash_balance_effect_flag: bool
    description: str
    ach_status: ACHStatus | None
    accrued_interest: float | None
    fees: Fees
    transaction_item: TransactionItem


# User Info and Preferences

# Watchlist
