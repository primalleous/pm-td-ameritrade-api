from typing import List

from pydantic import Field, field_validator, SerializeAsAny
from td.enums.orders import (
    AssetType,
    CashEquivalentType,
    CurrencyType,
    MutualFundType,
    OptionSide,
)
from td.models.base_api_model import BaseApiModel


class BaseInstrument(BaseApiModel):
    asset_type: str | AssetType
    cusip: str | None = None
    description: str | None = None
    symbol: str

    @field_validator("asset_type")
    @classmethod
    def validate_asset_type(cls, asset_type):
        return cls.validate_str_enum(asset_type, AssetType)


class OptionDeliverable(BaseInstrument):
    symbol: str
    deliverable_units: int
    currency_type: str | CurrencyType
    asset_type: str | AssetType

    @field_validator("currency_type")
    @classmethod
    def validate_currency_type(cls, currency_type):
        return cls.validate_str_enum(currency_type, CurrencyType)


class EquityInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.EQUITY.value


class OptionInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.OPTION.value
    put_call: str | OptionSide | None = None
    underlying_symbol: str | None = None
    option_multiplier: int | None = None
    option_deliverables: SerializeAsAny[List[OptionDeliverable]] | None = None

    @field_validator("put_call")
    @classmethod
    def validate_option_side(cls, put_call):
        return cls.validate_str_enum(put_call, OptionSide)


class IndexInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.INDEX.value


class MutualFundInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.MUTUAL_FUND.value
    type_: str | MutualFundType = Field(alias="type")

    @field_validator("type_")
    @classmethod
    def validate_type_(cls, type_):
        return cls.validate_str_enum(type_, MutualFundType)


class CashEquivalentInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.CASH_EQUIVALENT.value
    type_: str | CashEquivalentType = Field(alias="type")

    @field_validator("type_")
    @classmethod
    def validate_type_(cls, type_):
        return cls.validate_str_enum(type_, CashEquivalentType)


class FixedIncomeInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.FIXED_INCOME.value
    maturity_date: str
    variable_rate: int
    factor: int


class CurrencyInstrument(BaseInstrument):
    asset_type: str | AssetType = AssetType.CURRENCY.value


class InstrumentFactory:
    @staticmethod
    def create_instrument(asset_type: AssetType, instrument: dict):
        if asset_type == AssetType.EQUITY:
            return EquityInstrument(**instrument)
        elif asset_type == AssetType.OPTION:
            return OptionInstrument(**instrument)
        elif asset_type == AssetType.INDEX:
            return IndexInstrument(**instrument)
        elif asset_type == AssetType.MUTUAL_FUND:
            return MutualFundInstrument(**instrument)
        elif asset_type == AssetType.CASH_EQUIVALENT:
            return CashEquivalentInstrument(**instrument)
        elif asset_type == AssetType.FIXED_INCOME:
            return FixedIncomeInstrument(**instrument)
        elif asset_type == AssetType.CURRENCY:
            return CurrencyInstrument(**instrument)
        else:
            raise ValueError(f"Invalid asset type: {asset_type}")
