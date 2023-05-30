from datetime import datetime
from typing import ForwardRef, List

from pydantic import validator
from td.enums.orders import (
    ActivityType,
    AssetType,
    ComplexOrderStrategyType,
    Duration,
    ExecutionType,
    OrderInstruction,
    OrderStatus,
    OrderStrategyType,
    OrderType,
    PositionEffect,
    PriceLinkBasis,
    PriceLinkType,
    QuantityType,
    RequestedDestination,
    Session,
    SpecialInstruction,
    StopPriceLinkBasis,
    StopPriceLinkType,
    StopType,
    TaxLotMethod,
)
from td.models.base_api_model import BaseApiModel
from td.models.instruments import BaseInstrument, InstrumentFactory


class BaseOrdersModel(BaseApiModel):
    pass


class CancelTime(BaseOrdersModel):
    date: str
    short_format: bool = False


class ExecutionLegs(BaseOrdersModel):
    leg_id: int
    quantity: int
    mismarked_quantity: int
    price: int
    time: str


class OrderActivityExecution(BaseOrdersModel):
    activity_type: str | ActivityType
    execution_type: str | ExecutionType = ExecutionType.FILL
    quantity: int
    order_remaining_quantity: int
    execution_legs: List[ExecutionLegs]

    @validator("activity_type")
    def validate_activity_type(cls, activity_type):
        return cls.validate_str_enum(activity_type, ActivityType)

    @validator("execution_type")
    def validate_execution_type(cls, execution_type):
        return cls.validate_str_enum(execution_type, ExecutionType)


class OrderLeg(BaseOrdersModel):
    order_leg_type: str | AssetType
    leg_id: int | None = None
    instrument: BaseInstrument  #
    instruction: str | OrderInstruction
    position_effect: str | PositionEffect | None = None
    quantity: int
    quantity_type: str | QuantityType | None = None

    @validator("order_leg_type")
    def validate_order_leg_type(cls, order_leg_type):
        return cls.validate_str_enum(order_leg_type, AssetType)

    @validator("instrument", pre=True)
    def set_instrument_type(cls, v, values):
        if isinstance(v, BaseInstrument):
            return v

        order_leg_type = values.get("order_leg_type")
        asset_type = AssetType.value_mapping().get(order_leg_type)
        if asset_type:
            return InstrumentFactory.create_instrument(asset_type, instrument=v)
        else:
            raise ValueError(f"Unknown asset type. Instrument: {v}")

    @validator("instruction")
    def validate_instruction(cls, instruction):
        return cls.validate_str_enum(instruction, OrderInstruction)

    @validator("position_effect")
    def validate_position_effect(cls, position_effect):
        return cls.validate_str_enum(position_effect, PositionEffect)

    @validator("quantity_type")
    def validate_quantity_type(cls, quantity_type):
        return cls.validate_str_enum(quantity_type, QuantityType)


Order = ForwardRef("Order")


class Order(BaseOrdersModel):
    session: str | Session | None = None
    duration: str | Duration | None = None
    order_type: str | OrderType | None = None
    cancel_time: CancelTime | None = None
    complex_order_strategy_type: str | ComplexOrderStrategyType | None = None
    quantity: int | None = None
    filled_quantity: int | None = None
    remaining_quantity: int | None = None
    requested_destination: str | RequestedDestination | None = None
    destination_link_name: str | None = None
    release_time: datetime | None = None
    stop_price: float | None = None
    stop_price_link_basis: str | StopPriceLinkBasis | None = None
    stop_price_link_type: str | StopPriceLinkType | None = None
    stop_price_offset: float | None = None
    stop_type: str | StopType | None = None
    price_link_basis: str | PriceLinkBasis | None = None
    price_link_type: str | PriceLinkType | None = None
    price: float | None = None
    tax_lot_method: str | TaxLotMethod | None = None
    order_leg_collection: List[OrderLeg]  #
    activation_price: float | None = None
    special_instruction: str | SpecialInstruction | None = None
    order_strategy_type: str | OrderStrategyType | None = None
    order_id: int | None = None
    cancelable: bool | None = None
    editable: bool | None = None
    status: str | OrderStatus | None = None
    entered_time: datetime | None = None
    close_time: datetime | None = None
    account_id: str | None = None
    order_activity_collection: List[OrderActivityExecution] | None = None  #
    replacing_order_collection: List[Order] | None = None  #
    child_order_strategies: List[Order] | None = None  #
    status_description: str | None = None
    tag: str | None = None

    @validator("price", pre=True)
    def check_price_and_order_type(cls, v, values):
        """Validate price based on OrderType."""
        # TODO: add other checks for other order types
        if values.get("order_type") == OrderType.LIMIT and v is None:
            raise ValueError("price cannot be None for a limit order")
        return v

    @validator("session", "duration", "order_type", pre=True)
    def check_order_strategy_type(cls, v, values):
        """Validate session, duration, & order_type based on order_strategy_type."""
        if values.get("order_strategy_type") != "OCO" and v is None:
            raise ValueError(
                "session, duration, and order_type cannot be None if order_strategy_type is not 'OCO'"
            )
        return v

    @validator("session")
    def validate_session(cls, session):
        return cls.validate_str_enum(session, Session)

    @validator("duration")
    def validate_duration(cls, duration):
        return cls.validate_str_enum(duration, Duration)

    @validator("order_type")
    def validate_order_type(cls, order_type):
        return cls.validate_str_enum(order_type, OrderType)

    @validator("complex_order_strategy_type")
    def validate_complex_order_strategy_type(cls, complex_order_strategy_type):
        return cls.validate_str_enum(
            complex_order_strategy_type, ComplexOrderStrategyType
        )

    @validator("requested_destination")
    def validate_requested_destination(cls, requested_destination):
        return cls.validate_str_enum(requested_destination, RequestedDestination)

    @validator("stop_price_link_basis")
    def validate_stop_price_link_basis(cls, stop_price_link_basis):
        return cls.validate_str_enum(stop_price_link_basis, StopPriceLinkBasis)

    @validator("stop_price_link_type")
    def validate_stop_price_link_type(cls, stop_price_link_type):
        return cls.validate_str_enum(stop_price_link_type, StopPriceLinkType)

    @validator("price_link_basis")
    def validate_price_link_basis(cls, price_link_basis):
        return cls.validate_str_enum(price_link_basis, PriceLinkBasis)

    @validator("price_link_type")
    def validate_price_link_type(cls, price_link_type):
        return cls.validate_str_enum(price_link_type, PriceLinkType)

    @validator("tax_lot_method")
    def validate_tax_lot_method(cls, tax_lot_method):
        return cls.validate_str_enum(tax_lot_method, TaxLotMethod)

    @validator("special_instruction")
    def validate_special_instruction(cls, special_instruction):
        return cls.validate_str_enum(special_instruction, SpecialInstruction)

    @validator("order_strategy_type")
    def validate_order_strategy_type(cls, order_strategy_type):
        return cls.validate_str_enum(order_strategy_type, OrderStrategyType)

    @validator("status")
    def validate_status(cls, status):
        return cls.validate_str_enum(status, OrderStatus)

    # TODO: Logic around when direct routing can be specified
    #  Not sure if this is even possible
    #
    #  https://invest.ameritrade.com/grid/p/site#r=jPage/cgi-bin/apps/u/DirectRouting
    #  Directy routing is not available for equity orders
    #  Direct routing is available for single-leg options orders
    # @validator('order_leg_collection', pre=True)
    # def check_requested_destination(cls, v, values):
    #     """Validate requested destination for equity orders."""
    #     # TODO: add other checks for other asset types
    #     if v[0].order_leg_type == AssetType.EQUITY:
    #         if values.get('requested_destination') not in (
    #                 [RequestedDestination.INET,
    #                  RequestedDestination.ECN_ARCA,
    #                  RequestedDestination.AUTO
    #                 ]
    #             ):
    #             raise ValueError(
    #                 "Equity orders can only have a requestedDestination of 'INET', 'ECN_ARCA', 'AUTO'.")
    #     return v


Order.update_forward_refs()
