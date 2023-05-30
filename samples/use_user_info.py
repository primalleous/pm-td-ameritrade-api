from pprint import pprint
from td.client import TdAmeritradeClient
from td.config import TdConfiguration
from td.enums.orders import Duration
from td.enums.enums import DefaultAdvancedToolLaunch
from td.enums.orders import OrderInstruction
from td.enums.orders import Session
from td.enums.orders import StopPriceLinkType
from td.enums.orders import OrderType
from td.enums.orders import TaxLotMethod
from td.enums.enums import AuthTokenTimeout
from td.utils.user_preferences import UserPreferences

# A config object
config = TdConfiguration("config-example/config.ini")

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()

account_number = config.accounts.default_account

# Initialize the `UserInfo` service.
user_info_service = td_client.user_info()

# Grab the preferences for a specific account.
pprint(user_info_service.get_preferences(account_id=account_number))

# Grab the streamer subscription keys.
pprint(user_info_service.get_streamer_subscription_keys(account_ids=[account_number]))

# Grab User Principals.
pprint(user_info_service.get_user_principals())

# Method 1, Update the User Preferences.
user_info_service.update_user_preferences(
    account_id=account_number,
    preferences={
        "authTokenTimeout": "EIGHT_HOURS",
        "defaultAdvancedToolLaunch": "NONE",
        "defaultEquityOrderDuration": "DAY",
        "defaultEquityOrderLegInstruction": "NONE",
        "defaultEquityOrderMarketSession": "NORMAL",
        "defaultEquityOrderPriceLinkType": "NONE",
        "defaultEquityOrderType": "LIMIT",
        "defaultEquityQuantity": 0,
        "equityTaxLotMethod": "FIFO",
        "expressTrading": True,
        "mutualFundTaxLotMethod": "FIFO",
        "optionTaxLotMethod": "FIFO",
    },
)

# Method 2, Update the User Preferences.
my_preferences = {
    "default_equity_order_leg_instruction": OrderInstruction.BUY,
    "default_equity_order_type": OrderType.MARKET,
    "default_equity_order_price_link_type": StopPriceLinkType.NONE,
    "default_equity_order_duration": Duration.DAY,
    "default_equity_order_market_session": Session.NORMAL,
    "mutual_fund_tax_lot_method": TaxLotMethod.FIFO,
    "option_tax_lot_method": TaxLotMethod.FIFO,
    "equity_tax_lot_method": TaxLotMethod.FIFO,
    "default_advanced_tool_launch": DefaultAdvancedToolLaunch.TA,
    "auth_token_timeout": AuthTokenTimeout.EIGHT_HOURS,
}

# Define a new data class that will store our preferences.
my_user_preferences = UserPreferences(**my_preferences)

user_info_service.update_user_preferences(
    account_id=account_number, preferences=my_user_preferences.to_dict()
)


# Previous example doesn't work, not sure why
# all values in enums match api spec on tda, must be a specific combination

# Method 2, Update the User Preferences.
# my_preferences = {
#     'default_equity_order_leg_instruction': Instruction.Buy,
#     'default_equity_order_type': OrderType.Market,
#     'default_equity_order_price_link_type': StopPriceLinkType.Percent,
#     'default_equity_order_duration': Duration.NoneSpecified,
#     'default_equity_order_market_session': Session.Normal,
#     'mutual_fund_tax_lot_method': TaxLotMethod.FIFO,
#     'option_tax_lot_method': TaxLotMethod.FIFO,
#     'equity_tax_lot_method': TaxLotMethod.FIFO,
#     'default_advanced_tool_launch': DefaultAdvancedToolLaunch.Ta,
#     'auth_token_timeout': AuthTokenTimeout.EightHours
# }
