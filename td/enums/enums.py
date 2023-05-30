from enum import Enum


class _BaseEnum(Enum):
    """Base class for custom Enum classes."""

    @classmethod
    def all_values(cls):
        """Return a list containing all values as strings"""
        return [str(member.value) for member in cls]

    @classmethod
    def value_mapping(cls):
        """
        Return a dictionary mapping enum values to their corresponding names.

        The mapping is cached for performance.
        """
        try:
            return cls._value_mapping
        except AttributeError:
            cls._value_mapping = {
                str(member.value): cls[str(member.name)] for member in cls
            }
            return cls._value_mapping

    @classmethod
    def key_mapping(cls):
        """
        Return a dictionary mapping enum names to their corresponding values.

        The mapping is cached for performance.
        """
        try:
            return cls._key_mapping
        except AttributeError:
            cls._key_mapping = {
                cls[str(member.name)]: str(member.value) for member in cls
            }
            return cls._key_mapping


class QOSLevel(_BaseEnum):
    """Quality of service levels"""

    #: 500ms between updates. Fastest available
    EXPRESS = "0"

    #: 750ms between updates
    REAL_TIME = "1"

    #: 1000ms between updates. Default value.
    FAST = "2"

    #: 1500ms between updates
    MODERATE = "3"

    #: 3000ms between updates
    SLOW = "4"

    #: 5000ms between updates
    DELAYED = "5"


class MoversDirection(_BaseEnum):
    """Represents the direction options for the
    `Movers` service.

    Usage
    ----
        >>> from td.enums import Directions
        >>> Directions.Up.value
    """

    UP = "up"
    DOWN = "down"


class MoversChange(_BaseEnum):
    """Represents the change options for the
    `Movers` service.

    Usage
    ----
        >>> from td.enums import Change
        >>> Change.Percent.value
    """

    PERCENT = "percent"
    VALUE = "value"


class MoversIndex(_BaseEnum):
    """Represents the change options for the
    `Movers` service.

    Usage
    ----
        >>> from td.enums import Change
        >>> Change.Percent.value
    """

    COMPX = "$COMPX"
    DJX = "$DJI"
    SPX = "$SPX.X"


class QueryTransactionType(_BaseEnum):
    ALL = "ALL"
    TRADE = "TRADE"
    BUY_ONLY = "BUY_ONLY"
    SELL_ONLY = "SELL_ONLY"
    CASH_IN_OR_CASH_OUT = "CASH_IN_OR_CASH_OUT"
    CHECKING = "CHECKING"
    DIVIDEND = "DIVIDEND"
    INTEREST = "INTEREST"
    OTHER = "OTHER"
    ADVISOR_FEES = "ADVISOR_FEES"


class ResponseTransactionType(_BaseEnum):
    TRADE = "TRADE"
    RECEIVE_AND_DELIVER = "RECEIVE_AND_DELIVER"
    DIVIDEND_OR_INTEREST = "DIVIDEND_OR_INTEREST"
    ACH_RECEIPT = "ACH_RECEIPT"
    ACH_DISBURSEMENT = "ACH_DISBURSEMENT"
    CASH_RECEIPT = "CASH_RECEIPT"
    CASH_DISBURSEMENT = "CASH_DISBURSEMENT"
    ELECTRONIC_FUND = "ELECTRONIC_FUND"
    WIRE_OUT = "WIRE_OUT"
    WIRE_IN = "WIRE_IN"
    JOURNAL = "JOURNAL"
    MEMORANDUM = "MEMORANDUM"
    MARGIN_CALL = "MARGIN_CALL"
    MONEY_MARKET = "MONEY_MARKET"
    SMA_ADJUSTMENT = "SMA_ADJUSTMENT"


class ACHStatus(_BaseEnum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CANCEL = "Cancel"
    ERROR = "Error"


class Markets(_BaseEnum):
    """Represents the different markets you can request
    hours for the `MarketHours` service.

    Usage
    ----
        >>> from td.enums import Markets
        >>> Markets.Bond.Value
    """

    BOND = "BOND"
    EQUITY = "EQUITY"
    OPTION = "OPTION"
    FOREX = "FOREX"
    FUTURES = "FUTURES"


class Projections(_BaseEnum):
    """Represents the different search types you can use for
    the `Instruments` service.

    Usage
    ----
        >>> from td.enums import Projections
        >>> Projections.Bond.Value
    """

    SYMBOL_SEARCH = "symbol-search"
    SYMBOL_REGEX = "symbol-regex"
    DESCRIPTION_SEARCH = "desc-search"
    DESCRIPTION_REGEX = "desc-regex"
    FUNDAMENTAL = "fundamental"


class DefaultOrderType(_BaseEnum):
    """Represents the different Default Order Type
    for the `UserInfo` service.

    Usage
    ----
        >>> from td.enums import DefaultOrderType
        >>> DefaultOrderType.Market.Value
    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"
    MARKET_ON_CLOSE = "MARKET_ON_CLOSE"
    NONE_SPECIFIED = "NONE"


class DefaultAdvancedToolLaunch(_BaseEnum):
    """Represents the different Default Advanced Tool
    Lauch for the `UserInfo` service.

    Usage
    ----
        >>> from td.enums import DefaultAdvancedToolLaunch
        >>> DefaultAdvancedToolLaunch.Tos.Value
    """

    TA = "TA"
    NO = "N"
    YES = "Y"
    TOS = "TOS"
    CC2 = "CC2"
    NONE_SPECIFIED = "NONE"


class AuthTokenTimeout(_BaseEnum):
    """Represents the different Auth Token Timeout
    properties for the `UserInfo` service.

    Usage
    ----
        >>> from td.enums import AuthTokenTimeout
        >>> AuthTokenTimeout.FiftyFiveMinutes.Value
    """

    FIFTY_FIVE_MINUTES = "FIFTY_FIVE_MINUTES"
    TWO_HOURS = "TWO_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    EIGHT_HOURS = "EIGHT_HOURS"


class FrequencyType(_BaseEnum):
    """Represents the different chart frequencies
    for the `PriceHistory` service.

    Usage
    ----
        >>> from td.enums import PriceFrequency
        >>> PriceFrequency.Daily.Value
    """

    MINUTE = "minute"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PeriodType(_BaseEnum):
    """Represents the different chart periods
    for the `PriceHistory` service.

    Usage
    ----
        >>> from td.enums import PriceFrequency
        >>> PeriodType.Daily.Value
    """

    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    YEAR_TO_DATE = "ytd"


class StrategyType(_BaseEnum):
    """Represents the different strategy types
    when querying the `OptionChain` service.

    Usage
    ----
        >>> from td.enums import StrategyType
        >>> StrategyType.ANALYTICAL.value
    """

    ANALYTICAL = "ANALYTICAL"
    BUTTERFLY = "BUTTERFLY"
    CALENDAR = "CALENDAR"
    COLLAR = "COLLAR"
    CONDOR = "CONDOR"
    COVERED = "COVERED"
    DIAGONAL = "DIAGONAL"
    ROLL = "ROLL"
    SINGLE = "SINGLE"
    STRADDLE = "STRADDLE"
    STRANGLE = "STRANGLE"
    VERTICAL = "VERTICAL"


class OptionRange(_BaseEnum):
    """Represents the different option range types
    when querying the `OptionChain` service.

    Usage
    ----
        >>> from td.enums import OptionRange
        >>> OptionRange.IN_THE_MONEY.value
    """

    ALL = "ALL"
    IN_THE_MONEY = "ITM"
    NEAR_THE_MONEY = "NTM"
    OUT_THE_MONEY = "OTM"
    STRIKES_ABOVE_MARKET = "SAK"
    STRIKES_BELOW_MARKET = "SBK"
    STRIKES_NEAR_MARKET = "SNK"


class ExpirationMonth(_BaseEnum):
    """Represents the different option expiration months
    when querying the `OptionChain` service.

    Usage
    ----
        >>> from td.enums import ExpirationMonth
        >>> ExpirationMonth.JANUARY.value
    """

    ALL = "ALL"
    JANUARY = "JAN"
    FEBRUARY = "FEB"
    MARCH = "MAR"
    APRIL = "APR"
    MAY = "MAY"
    JUNE = "JUN"
    JULY = "JUL"
    AUGUST = "AUG"
    SEPTEMBER = "SEP"
    OCTOBER = "OCT"
    NOVEMBER = "NOV"
    DECEMBER = "DEC"


class ContractType(_BaseEnum):
    """Represents the different option contract types
    when querying the `OptionChain` service.

    Usage
    ----
        >>> from td.enums import ContractType
        >>> ContractType.CALL.value
    """

    ALL = "ALL"
    CALL = "CALL"
    PUT = "PUT"


class OptionType(_BaseEnum):
    """Represents the different option types
    when querying the `OptionChain` service.

    Usage
    ----
        >>> from td.enums import OptionType
        >>> OptionType.CALL.value
    """

    ALL = "ALL"
    STANDARD_CONTRACTS = "S"
    NON_STANDARD_CONTRACTS = "NS"


# TODO: Unsure if accurate due to no descriptions (e.g. is Mutual Fund, MUTUAL_FUND)
class QuoteAssetType(_BaseEnum):
    """Represents the different quote Asset types.

    Usage
    ----
        >>> from td.enums import AssetType
        >>> AssetType.EQUITY.Value
    """

    MUTUALFUND = "MUTUAL_FUND"
    FUTURE = "FUTURE"
    FUTUREOPTIONS = "FUTURE_OPTIONS"
    INDEX = "INDEX"
    OPTION = "OPTION"
    FOREX = "FOREX"
    ETF = "ETF"
    EQUITY = "EQUITY"


class NewsServices(_BaseEnum):
    """Represents the different streaming level news
    services.

    Usage
    ----
        >>> from td.enums import NewsServices
        >>> NewsServices.HEADLINE.Value
    """

    HEADLINE = "NEWS_HEADLINE"


class ChartServices(_BaseEnum):
    """Represents the different streaming chart
    services.

    Usage
    ----
        >>> from td.enums import ChartServices
        >>> ChartServices.ChartEquity.Value
    """

    CHART_EQUITY = "CHART_EQUITY"
    CHART_FUTURES = "CHART_FUTURES"
    CHART_OPTIONS = "CHART_OPTIONS"


class ChartHistoryServices(_BaseEnum):
    """Represents the different streaming chart
    history services.

    Usage
    ----
        >>> from td.enums import ChartHistoryServices
        >>> ChartHistoryServices.CHART_HISTORY_FUTURES.Value
    """

    CHART_HISTORY_FUTURES = "CHART_HISTORY_FUTURES"


class LevelOneServices(_BaseEnum):
    """Represents the different streaming level one
    services.

    Usage
    ----
        >>> from td.enums import LevelOneServices
        >>> LevelOneServices.FUTURES.Value
    """

    EQUITY = "QUOTE"
    OPTIONS = "OPTION"
    FUTURES = "LEVELONE_FUTURES"
    FOREX = "LEVELONE_FOREX"
    FUTURES_OPTIONS = "LEVELONE_FUTURES_OPTIONS"


class LevelTwoServices(_BaseEnum):
    """Represents the different streaming level two
    services.

    Usage
    ----
        >>> from td.enums import LevelTwoServices
        >>> LevelTwoServices.FUTURES.Value
    """

    EQUITY = "LISTED_BOOK"
    OPTIONS = "OPTIONS_BOOK"
    NASDAQ = "NASDAQ_BOOK"
    FUTURES = "FUTURES_BOOK"
    FOREX = "FOREX_BOOK"
    FUTURES_OPTIONS = "FUTURES_OPTIONS_BOOK"


class TimesaleServices(_BaseEnum):
    """Represents the different streaming timesale
    services.

    Usage
    ----
        >>> from td.enums import TimesaleServices
        >>> TimesaleServices.TimesaleEquity.Value
    """

    TIMESALE_EQUITY = "TIMESALE_EQUITY"
    TIMESALE_FOREX = "TIMESALE_FOREX"
    TIMESALE_FUTURES = "TIMESALE_FUTURES"
    TIMESALE_OPTIONS = "TIMESALE_OPTIONS"


class ActivesServices(_BaseEnum):
    """Represents the different streaming actives
    services.

    Usage
    ----
        >>> from td.enums import ActivesServices
        >>> ActivesServices.ActivesNasdaq.Value
    """

    ACTIVES_NASDAQ = "ACTIVES_NASDAQ"
    ACTIVES_NYSE = "ACTIVES_NYSE"
    ACTIVES_OPTIONS = "ACTIVES_OPTIONS"
    ACTIVES_OTCBB = "ACTIVES_OTCBB"


class ActivesVenues(_BaseEnum):
    """Represents the different streaming actives
    venues.

    Usage
    ----
        >>> from td.enums import ActivesVenues
        >>> ActivesVenues.Nasdaq.Value
    """

    NASDAQ_EXCHANGE = "NASDAQ"
    NEW_YORK_STOCK_EXCHANGE = "NYSE"
    OVER_THE_COUNTER_BULLETIN_BOARD = "OTCBB"
    CALLS = "CALLS"
    PUTS = "PUTS"
    OPTIONS = "OPTS"
    CALLS_DESC = "CALLS-DESC"
    PUTS_DESC = "PUTS-DESC"
    OPTIONS_DESC = "OPTS-DESC"


class ActivesDurations(_BaseEnum):
    """Represents the different durations for the
    Actives Service.

    Usage
    ----
        >>> from td.enums import ActivesDurations
        >>> ActivesDurations...
    """

    ALL = "ALL"
    SIXTY_SECONDS = "60"
    THREE_HUNDRED_SECONDS = "300"
    SIX_HUNDRED_SECONDS = "600"
    EIGHTEEN_HUNDRED_SECONDS = "1800"
    THIRTY_SIX_HUNDRED_SECONDS = "3600"


class ChartFuturesFrequencies(_BaseEnum):
    """Represents the different frequencies for the
    Chart History Futures streaming service.

    Usage
    ----
        >>> from td.enums import ChartFuturesFrequencies
        >>> ChartFuturesFrequencies.OneMinute.Value
    """

    ONE_MINUTE = "m1"
    FIVE_MINUTE = "m5"
    TEN_MINUTE = "m10"
    THIRTY_MINUTE = "m30"
    ONE_HOUR = "h1"
    ONE_DAY = "d1"
    ONE_WEEK = "w1"
    ONE_MONTH = "n1"


class ChartFuturesPeriods(_BaseEnum):
    """Represents the different periods for the
    Chart History Futures streaming service.

    Usage
    ----
        >>> from td.enums import ChartFuturesPeriods
        >>> ChartFuturesPeriods.OneDay.Value
    """

    ONE_DAY = "d1"
    FIVE_DAY = "d5"
    FOUR_WEEKS = "w4"
    TEN_MONTHS = "n10"
    ONE_YEAR = "y1"
    TEN_YEAR = "y10"


class LevelTwoQuotes(_BaseEnum):
    """Represents the Level Two Quotes Fields.

    Usage
    ----
        >>> from td.enums import LevelTwoQuotes
        >>> LevelTwoQuotes...
    """

    KEY = 0
    TIME = 1
    DATA = 2


class StreamApiCommands(_BaseEnum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    QOS = "QOS"
    SUBS = "SUBS"
    ADD = "ADD"
    UNSUBS = "UNSUBS"
    STREAM = "STREAM"
    VIEW = "VIEW"


class StreamApiResponse(_BaseEnum):
    RESPONSE = "response"
    DATA = "data"
    NOTIFY = "notify"
    SNAPSHOT = "snapshot"


class ServiceState(_BaseEnum):
    ACKED = "acked"  # attempting to subscribe
    SUBSCRIBED = "subscribed"


# class LevelTwoOptions(_BaseEnum):
#     """Represents the Level Two Options Fields.

#     Usage
#     ----
#         >>> from td.enums import LevelTwoOptions
#         >>> LevelTwoOptions...
#     """
#     KEY = 0
#     TIME = 1
#     DATA = 2

# class ChartEquityFields(_BaseEnum):
#     """Represents the different streaming chart
#     equity fields.

#     Usage
#     ----
#         >>> from td.enums import ChartEquityFields
#         >>> ChartEquityFields...
#     """

#     SYMBOL = 0
#     OPEN_PRICE = 1
#     HIGH_PRICE = 2
#     LOW_PRICE = 3
#     CLOSE_PRICE = 4
#     VOLUME = 5
#     SEQUENCE = 6
#     CHART_TIME = 7
#     CHART_DAY = 8


# class ChartFuturesOrOptionsFields(_BaseEnum):
#     """Represents the different streaming chart
#     futures fields.

#     Usage
#     ----
#         >>> from td.enums import ChartFuturesOrOptionsFields
#         >>> ChartFuturesOrOptionsFields...
#     """

#     SYMBOL = 0
#     CHART_TIME = 1
#     OPEN_PRICE = 2
#     HIGH_PRICE = 3
#     LOW_PRICE = 4
#     CLOSE_PRICE = 5
#     VOLUME = 6

# class Timesale(_BaseEnum):
#     """Represents the different streaming timesale
#     fields.

#     Usage
#     ----
#         >>> from td.enums import Timesale
#         >>> Timesale...
#     """

#     SYMBOL = 0
#     TRADE_TIME = 1
#     LAST_PRICE = 2
#     LAST_SIZE = 3
#     LAST_SEQUENCE = 4

# class DefaultOrderPriceLinkType(_BaseEnum):
#     """Represents the different Default Order Price Link Type
#     for the `UserInfo` service.

#     Usage
#     ----
#         >>> from td.enums import DefaultOrderPriceLinkType
#         >>> DefaultOrderPriceLinkType.Value.Value
#     """

#     Value = "VALUE"
#     Percent = "PERCENT"
#     NoneSpecified = "NONE"


# class DefaultOrderDuration(_BaseEnum):
#     """Represents the different Default Order Duration
#     for the `UserInfo` service.

#     Usage
#     ----
#         >>> from td.enums import DefaultOrderDuration
#         >>> DefaultOrderDuration.Day.Value
#     """

#     Day = "DAY"
#     GoodTillCancel = "GOOD_TILL_CANCEL"
#     FillOrKill = "FILL_OR_KILL"
#     NoneSpecified = "NONE"


# class DefaultOrderMarketSession(_BaseEnum):
#     """Represents the different Default Order Market Session
#     for the `UserInfo` service.

#     Usage
#     ----
#         >>> from td.enums import DefaultOrderMarketSession
#         >>> DefaultOrderMarketSession.Day.Value
#     """

#     Am = "AM"
#     Pm = "PM"
#     Normal = "NORMAL"
#     Seamless = "SEAMLESS"
#     NoneSpecified = "NONE"


# class TaxLotMethod(_BaseEnum):
#     """Represents the different Tax Lot Methods
#     for the `UserInfo` service.

#     Usage
#     ----
#         >>> from td.enums import MutualFundTaxLotMethod
#         >>> MutualFundTaxLotMethod.Day.Value
#     """

#     Fifo = "FIFO"
#     Lifo = "LIFO"
#     HighCost = "HIGH_COST"
#     LowCost = "LOW_COST"
#     MinimumTax = "MINIMUM_TAX"
#     AverageCost = "AVERAGE_COST"
#     NoneSpecified = "NONE"

# class DefaultOrderLegInstruction(_BaseEnum):
#     """Represents the different Default Order Leg Instructions
#     for the `UserInfo` service.

#     Usage
#     ----
#         >>> from td.enums import DefaultOrderLegInstruction
#         >>> DefaultOrderLegInstruction.Sell.Value
#     """

#     Buy = "BUY"
#     Sell = "SELL"
#     BuyToCover = "BUY_TO_COVER"
#     SellShort = "SELL_SHORT"
#     NoneSpecified = "NONE"

# class ChartHistoryResponse(_BaseEnum):
#     """Represents the nested response values you get
#     from the chart history endpoint.

#     Usage
#     ----
#         >>> from td.enums import ChartHistoryResponse
#         >>> ChartHistoryResponse.TIMESTAMP.Value
#     """

#     TIMESTAMP = "0"
#     OPEN = "1"
#     HIGH = "2"
#     LOW = "3"
#     CLOSE = "4"
#     VOLUME = "5"

# class OrderStatus(_BaseEnum):
#     """Represents the different order status types
#     when querying the `Orders` service.

#     Usage
#     ----
#         >>> from td.enums import OrderStatus
#         >>> OrderStatus.Working.Value
#     """

#     AwaitingParentOrder = "AWAITING_PARENT_ORDER"
#     AwaitingCondition = "AWAITING_CONDITION"
#     AwaitingManualReview = "AWAITING_MANUAL_REVIEW"
#     Accepted = "ACCEPTED"
#     AwaitingUrOut = "AWAITING_UR_OUT"
#     PendingActivation = "PENDING_ACTIVATION"
#     Queded = "QUEUED"
#     Working = "WORKING"
#     Rejected = "REJECTED"
#     PendingCancel = "PENDING_CANCEL"
#     Canceled = "CANCELED"
#     PendingReplace = "PENDING_REPLACE"
#     Replaced = "REPLACED"
#     Filled = "FILLED"
#     Expired = "EXPIRED"


# class OrderStrategyType(_BaseEnum):
#     """Represents the different order strategy types
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import OrderStrategyType
#         >>> OrderStrategyType.Single.Value
#     """

#     Single = "SINGLE"
#     Oco = "OCO"
#     Trigger = "TRIGGER"


# class QuantityType(_BaseEnum):
#     """Represents the different order quantity types
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import QuantityType
#         >>> QuantityType.Dollars.Value
#     """

#     AllShares = "ALL_SHARES"
#     Dollars = "DOLLARS"
#     Shares = "SHARES"


# class AssetType(_BaseEnum):
#     """Represents the different order Asset types
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import AssetType
#         >>> AssetType.Equity.Value
#     """

#     Equity = "EQUITY"
#     Option = "OPTION"
#     Index = "INDEX"
#     MutualFund = "MUTUAL_FUND"
#     CashEquivalent = "CASH_EQUIVALENT"
#     FixedIncome = "FIXED_INCOME"
#     Currency = "CURRENCY"


# class ComplexOrderStrategyType(_BaseEnum):
#     """Represents the different order Asset types
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import ComplexOrderStrategyType
#         >>> ComplexOrderStrategyType.IronCondor.Value
#     """

#     NoneProvided = "NONE"
#     Covered = "COVERED"
#     Vertical = "VERTICAL"
#     BackRatio = "BACK_RATIO"
#     Calendar = "CALENDAR"
#     Diagonal = "DIAGONAL"
#     Straddle = "STRADDLE"
#     Strangle = "STRANGLE"
#     CollarSynthetic = "COLLAR_SYNTHETIC"
#     Butterfly = "BUTTERFLY"
#     Condor = "CONDOR"
#     IronCondor = "IRON_CONDOR"
#     VerticalRoll = "VERTICAL_ROLL"
#     CollarWithStock = "COLLAR_WITH_STOCK"
#     DoubleDiagonal = "DOUBLE_DIAGONAL"
#     UnbalancedButterfly = "UNBALANCED_BUTTERFLY"
#     UnbalancedCondor = "UNBALANCED_CONDOR"
#     UnbalancedIronCondor = "UNBALANCED_IRON_CONDOR"
#     UnbalancedVerticalRoll = "UNBALANCED_VERTICAL_ROLL"
#     Custom = "CUSTOM"


# class OrderInstructions(_BaseEnum):
#     """Represents the different order instructions
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import OrderInstructions
#         >>> OrderInstructions.SellShort.Value
#     """

#     Buy = "BUY"
#     Sell = "SELL"
#     BuyToCover = "BUY_TO_COVER"
#     SellShort = "SELL_SHORT"
#     BuyToOpen = "BUY_TO_OPEN"
#     BuyToClose = "BUY_TO_CLOSE"
#     SellToOpen = "SELL_TO_OPEN"
#     SellToClose = "SELL_TO_CLOSE"
#     Exchange = "EXCHANGE"


# class RequestedDestination(_BaseEnum):
#     """Represents the different order requested
#     destinations when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import RequestedDestination
#         >>> RequestedDestination.Cboe.Value
#     """

#     Inet = "INET"
#     EcnArca = "ECN_ARCA"
#     Cboe = "CBOE"
#     Amex = "AMEX"
#     Phlx = "PHLX"
#     Ise = "ISE"
#     Box = "BOX"
#     Nyse = "NYSE"
#     Nasdaq = "NASDAQ"
#     Bats = "BATS"
#     C2 = "C2"
#     Auto = "AUTO"


# class StopPriceLinkBasis(_BaseEnum):
#     """Represents the different stop price link basis
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import StopPriceLinkBasis
#         >>> StopPriceLinkBasis.Trigger.Value
#     """

#     Manual = "MANUAL"
#     Base = "BASE"
#     Trigger = "TRIGGER"
#     Last = "LAST"
#     Bid = "BID"
#     Ask = "ASK"
#     AskBid = "ASK_BID"
#     Mark = "MARK"
#     Average = "AVERAGE"


# class StopPriceLinkType(_BaseEnum):
#     """Represents the different stop price link type
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import StopPriceLinkType
#         >>> StopPriceLinkType.Trigger.Value
#     """

#     Value = "VALUE"
#     Percent = "PERCENT"
#     Tick = "TICK"


# class StopType(_BaseEnum):
#     """Represents the different stop type
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import StopType
#         >>> StopType.Standard.Value
#     """

#     Standard = "STANDARD"
#     Bid = "BID"
#     Ask = "ASK"
#     Last = "LAST"
#     Mark = "MARK"


# class PriceLinkBasis(_BaseEnum):
#     """Represents the different price link basis
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import PriceLinkBasis
#         >>> PriceLinkBasis.Manual.Value
#     """

#     Manual = "MANUAL"
#     Base = "BASE"
#     Trigger = "TRIGGER"
#     Last = "LAST"
#     Bid = "BID"
#     Ask = "ASK"
#     AskBid = "ASK_BID"
#     Mark = "MARK"
#     Average = "AVERAGE"


# class PriceLinkType(_BaseEnum):
#     """Represents the different price link type
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import PriceLinkType
#         >>> PriceLinkType.Trigger.Value
#     """

#     Value = "VALUE"
#     Percent = "PERCENT"
#     Tick = "TICK"


# class OrderType(_BaseEnum):
#     """Represents the different order type
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import OrderType
#         >>> OrderType.Market.Value
#     """

#     Market = "MARKET"
#     Limit = "LIMIT"
#     Stop = "STOP"
#     StopLimit = "STOP_LIMIT"
#     TrailingStop = "TRAILING_STOP"
#     MarketOnClose = "MARKET_ON_CLOSE"
#     Exercise = "EXERCISE"
#     TrailingStopLimit = "TRAILING_STOP_LIMIT"
#     NetDebit = "NET_DEBIT"
#     NetCredit = "NET_CREDIT"
#     NetZero = "NET_ZERO"


# class PositionEffect(_BaseEnum):
#     """Represents the different position effects
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import PositionEffect
#         >>> PositionEffect.Opening.Value
#     """

#     Opening = "OPENING"
#     Closing = "CLOSING"
#     Automatic = "AUTOMATIC"


# class OrderTaxLotMethod(_BaseEnum):
#     """Represents the different order tax lot methods
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import OrderTaxLotMethod
#         >>> OrderTaxLotMethod.Fifo.Value
#     """

#     Fifo = "FIFO"
#     Lifo = "LIFO"
#     HighCost = "HIGH_COST"
#     LowCost = "LOW_COST"
#     AverageCost = "AVERAGE_COST"
#     SpecificLot = "SPECIFIC_LOT"


# class SpecialInstructions(_BaseEnum):
#     """Represents the different order special instructions
#     when constructing and `Order` object.

#     Usage
#     ----
#         >>> from td.enums import SpecialInstructions
#         >>> SpecialInstructions.AllOrNone.Value
#     """

#     AllOrNone = "ALL_OR_NONE"
#     DoNotReduce = "DO_NOT_REDUCE"
#     AllOrNoneDoNotReduce = "ALL_OR_NONE_DO_NOT_REDUCE"


# class LevelOneQuotes(_BaseEnum):
#     """Represents the different fields for the Level One
#     Quotes Feed.

#     Usage
#     ----
#         >>> from td.enums import LevelOneQuotes
#         >>> LevelOneQuotes...
#     """

#     SYMBOL = 0
#     BID_PRICE = 1
#     ASK_PRICE = 2
#     LAST_PRICE = 3
#     BID_SIZE = 4
#     ASK_SIZE = 5
#     ASK_ID = 6
#     BID_ID = 7
#     TOTAL_VOLUME = 8
#     LAST_SIZE = 9
#     TRADE_TIME = 10
#     QUOTE_TIME = 11
#     HIGH_PRICE = 12
#     LOW_PRICE = 13
#     BID_TICK = 14
#     CLOSE_PRICE = 15
#     EXCHANGE_ID = 16
#     MARGINABLE = 17
#     SHORTABLE = 18
#     ISLAND_BID = 19
#     ISLAND_ASK = 20
#     ISLAND_VOLUME = 21
#     QUOTE_DAY = 22
#     TRADE_DAY = 23
#     VOLATILITY = 24
#     DESCRIPTION = 25
#     LAST_ID = 26
#     DIGITS = 27
#     OPEN_PRICE = 28
#     NET_CHANGE = 29
#     FIFTY_TWO_WEEK_HIGH = 30
#     FIFTY_TWO_WEEK_LOW = 31
#     PE_RATIO = 32
#     DIVIDEND_AMOUNT = 33
#     DIVIDEND_YIELD = 34
#     ISLAND_BID_SIZE = 35
#     ISLAND_ASK_SIZE = 36
#     NAV = 37
#     FUND_PRICE = 38
#     EXCHANGE_NAME = 39
#     DIVIDEND_DATE = 40
#     REGULAR_MARKET_QUOTE = 41
#     REGULAR_MARKET_TRADE = 42
#     REGULAR_MARKET_LAST_PRICE = 43
#     REGULAR_MARKET_LAST_SIZE = 44
#     REGULAR_MARKET_TRADE_TIME = 45
#     REGULAR_MARKET_TRADE_DAY = 46
#     REGULAR_MARKET_NET_CHANGE = 47
#     SECURITY_STATUS = 48
#     MARK = 49
#     QUOTE_TIME_IN_LONG = 50
#     TRADE_TIME_IN_LONG = 51
#     REGULAR_MARKET_TRADE_TIME_IN_LONG = 52


# class LevelOneOptions(_BaseEnum):
#     """Represents the different fields for the Level One
#     Options Feed.

#     Usage
#     ----
#         >>> from td.enums import LevelOneOptions
#         >>> LevelOneOptions...
#     """

#     SYMBOL = 0
#     DESCRIPTION = 1
#     BID_PRICE = 2
#     ASK_PRICE = 3
#     LAST_PRICE = 4
#     HIGH_PRICE = 5
#     LOW_PRICE = 6
#     CLOSE_PRICE = 7
#     TOTAL_VOLUME = 8
#     OPEN_INTEREST = 9
#     VOLATILITY = 10
#     QUOTE_TIME = 11
#     TRADE_TIME = 12
#     MONEY_INTRINSIC_VALUE = 13
#     QUOTE_DAY = 14
#     TRADE_DAY = 15
#     EXPIRATION_YEAR = 16
#     MULTIPLIER = 17
#     DIGITS = 18
#     OPEN_PRICE = 19
#     BID_SIZE = 20
#     ASK_SIZE = 21
#     LAST_SIZE = 22
#     NET_CHANGE = 23
#     STRIKE_PRICE = 24
#     CONTRACT_TYPE = 25
#     UNDERLYING = 26
#     EXPIRATION_MONTH = 27
#     DELIVERABLES = 28
#     TIME_VALUE = 29
#     EXPIRATION_DAY = 30
#     DAYS_TO_EXPIRATION = 31
#     DELTA = 32
#     GAMMA = 33
#     THETA = 34
#     VEGA = 35
#     RHO = 36
#     SECURITY_STATUS = 37
#     THEORETICAL_OPTION_VALUE = 38
#     UNDERLYING_PRICE = 39
#     UV_EXPIRATION_TYPE = 40
#     MARK = 41


# class LevelOneFutures(_BaseEnum):
#     """Represents the different fields for the Level One
#     Futures Feed.

#     Usage
#     ----
#         >>> from td.enums import LevelOneFutures
#         >>> LevelOneFutures...
#     """

#     SYMBOL = 0
#     BID_PRICE = 1
#     ASK_PRICE = 2
#     LAST_PRICE = 3
#     BID_SIZE = 4
#     ASK_SIZE = 5
#     ASK_ID = 6
#     BID_ID = 7
#     TOTAL_VOLUME = 8
#     LAST_SIZE = 9
#     QUOTE_TIME = 10
#     TRADE_TIME = 11
#     HIGH_PRICE = 12
#     LOW_PRICE = 13
#     CLOSE_PRICE = 14
#     EXCHANGE_ID = 15
#     DESCRIPTION = 16
#     LAST_ID = 17
#     OPEN_PRICE = 18
#     NET_CHANGE = 19
#     FUTURE_PERCENT_CHANGE = 20
#     EXHANGE_NAME = 21
#     SECURITY_STATUS = 22
#     OPEN_INTEREST = 23
#     MARK = 24
#     TICK = 25
#     TICK_AMOUNT = 26
#     PRODUCT = 27
#     FUTURE_PRICE_FORMAT = 28
#     FUTURE_TRADING_HOURS = 29
#     FUTURE_IS_TRADABLE = 30
#     FUTURE_MULTIPLIER = 31
#     FUTURE_IS_ACTIVE = 32
#     FUTURE_SETTLEMENT_PRICE = 33
#     FUTURE_ACTIVE_SYMBOL = 34
#     FUTURE_EXPIRATION_DATE = 35


# class LevelOneForex(_BaseEnum):
#     """Represents the different fields for the Level One
#     Forex Feed.

#     Usage
#     ----
#         >>> from td.enums import LevelOneForex
#         >>> LevelOneForex...
#     """

#     SYMBOL = 0
#     BID_PRICE = 1
#     ASK_PRICE = 2
#     LAST_PRICE = 3
#     BID_SIZE = 4
#     ASK_SIZE = 5
#     TOTAL_VOLUME = 6
#     LAST_SIZE = 7
#     QUOTE_TIME = 8
#     TRADE_TIME = 9
#     HIGH_PRICE = 10
#     LOW_PRICE = 11
#     CLOSE_PRICE = 12
#     EXCHANGE_ID = 13
#     DESCRIPTION = 14
#     OPEN_PRICE = 15
#     NET_CHANGE = 16
#     PERCENT_CHANGE = 17
#     EXCHANGE_NAME = 18
#     DIGITS = 19
#     SECURITY_STATUS = 20
#     TICK = 21
#     TICK_AMOUNT = 22
#     PRODUCT = 23
#     TRADING_HOURS = 24
#     IS_TRADABLE = 25
#     MARKET_MAKER = 26
#     FIFTY_TWO_WEEK_HIGH = 27
#     FIFTY_TWO_WEEK_LOW = 28
#     MARK = 29


# class NewsHeadlines(_BaseEnum):
#     """Represents the different fields for the News
#     Headline Feed.

#     Usage
#     ----
#         >>> from td.enums import NewsHeadlines
#         >>> NewsHeadlines...
#     """

#     SYMBOL = 0
#     ERROR_CODE = 1
#     STORY_DATETIME = 2
#     HEADLINE_ID = 3
#     STATUS = 4
#     HEADLINE = 5
#     STORY_ID = 6
#     COUNT_FOR_KEYWORD = 7
#     KEYWORD_ARRAY = 8
#     IS_HOT = 9
#     STORY_SOURCE = 10


# class LevelOneFuturesOptions(_BaseEnum):
#     """Represents the different fields for the Level
#     One Futures Options feed.

#     Usage
#     ----
#         >>> from td.enums import LevelOneFuturesOptions
#         >>> LevelOneFuturesOptions...
#     """

#     SYMBOL = 0
#     BID_PRICE = 1
#     ASK_PRICE = 2
#     LAST_PRICE = 3
#     BID_SIZE = 4
#     ASK_SIZE = 5
#     ASK_ID = 6
#     BID_ID = 7
#     TOTAL_VOLUME = 8
#     LAST_SIZE = 9
#     QUOTE_TIME = 10
#     TRADE_TIME = 11
#     HIGH_PRICE = 12
#     LOW_PRICE = 13
#     CLOSE_PRICE = 14
#     EXCHANGE_ID = 15
#     DESCRIPTION = 16
#     LAST_ID = 17
#     OPEN_PRICE = 18
#     NET_CHANGE = 19
#     FUTURE_PERCENT_CHANGE = 20
#     EXHANGE_NAME = 21
#     SECURITY_STATUS = 22
#     OPEN_INTEREST = 23
#     MARK = 24
#     TICK = 25
#     TICK_AMOUNT = 26
#     PRODUCT = 27
#     FUTURE_PRICE_FORMAT = 28
#     FUTURE_TRADING_HOURS = 29
#     FUTURE_IS_TRADABLE = 30
#     FUTURE_MULTIPLIER = 31
#     FUTURE_IS_ACTIVE = 32
#     FUTURE_SETTLEMENT_PRICE = 33
#     FUTURE_ACTIVE_SYMBOL = 34
#     FUTURE_EXPIRATION_DATE = 35
