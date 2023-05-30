from typing import List

from td.enums.orders import (
    AssetType,
    ComplexOrderStrategyType,
    Duration,
    OrderInstruction,
    OptionSide,
    OrderStrategyType,
    OrderType,
    PriceLinkBasis,
    PriceLinkType,
    RequestedDestination,
    Session,
    SpecialInstruction,
    StopPriceLinkBasis,
    StopPriceLinkType,
    StopType,
)
from td.models.orders import (
    Order,
    OrderLeg,
)

from td.models.instruments import (
    CashEquivalentInstrument,
    CurrencyInstrument,
    EquityInstrument,
    FixedIncomeInstrument,
    IndexInstrument,
    BaseInstrument,
    MutualFundInstrument,
    OptionInstrument,
    OptionDeliverable,
)


class OrderBuilder:
    """A builder class for constructing an `Order` object.

    This class provides methods for setting various attributes of an `Order` object,
    such as the session, order type, order strategy type, and order legs.

    Args:
        None

    Returns:
        None

    Example:
        To create a new order:
        ```
        order = (OrderBuilder()
            .set_order_type("LIMIT")
            .set_session("NORMAL")
            .set_duration("DAY")
            .set_price(350)
            .set_order_strategy_type("SINGLE")
            .add_equity_leg("BUY", "SPY", 1)
            ).build()
        ```
    """

    def __init__(self):
        self._legs: List[OrderLeg] = []
        self._replacing_order_collection: List[Order] = []
        self._child_order_strategies: List[Order] = []
        self._order: Order = None
        self._order_dict = {}

    def set_session(self, session: Session) -> "OrderBuilder":
        """Set the trading session for the order.

        Args:
            session (Session): The trading session for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["session"] = session
        return self

    def set_duration(self, duration: Duration) -> "OrderBuilder":
        """Set the duration for the order.

        Args:
            duration (Duration): The duration for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["duration"] = duration
        return self

    def set_order_type(self, order_type: OrderType) -> "OrderBuilder":
        """Set the order type for the order.

        Args:
            order_type (OrderType): The order type for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["order_type"] = order_type
        return self

    def set_price(self, price: float) -> "OrderBuilder":
        """Set the price for the order.

        Args:
            price (float): The price for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["price"] = price
        return self

    def set_order_strategy_type(
        self,
        order_strategy_type: OrderStrategyType,
    ) -> "OrderBuilder":
        """Set the order strategy type for the order.

        Args:
            order_strategy_type (OrderStrategyType): The order strategy type for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["order_strategy_type"] = order_strategy_type
        return self

    def set_complex_order_strategy_type(
        self,
        complex_order_strategy_type: ComplexOrderStrategyType,
    ) -> "OrderBuilder":
        """Set the complex order strategy type for the order.

        Args:
            complex_order_strategy_type (ComplexOrderStrategyType): The complex order strategy
                type for the order.

            Returns:
                OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["complex_order_strategy_type"] = complex_order_strategy_type
        return self

    def set_stop_price(self, stop_price: float) -> "OrderBuilder":
        """Set the stop price for the order.

        Args:
            stop_price (float): The stop price for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["stop_price"] = stop_price
        return self

    def set_stop_price_link_basis(
        self,
        stop_price_link_basis: StopPriceLinkBasis,
    ) -> "OrderBuilder":
        """Set the stop price link basis for the order.

        Args:
            stop_price_link_basis (StopPriceLinkBasis): The stop price link basis for the
                order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["stop_price_link_basis"] = stop_price_link_basis
        return self

    def set_stop_price_link_type(
        self,
        stop_price_link_type: StopPriceLinkType,
    ) -> "OrderBuilder":
        """Set the stop price link type for the order.

        Args:
            stop_price_link_type (StopPriceLinkType): The stop price link type for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["stop_price_link_type"] = stop_price_link_type
        return self

    def set_stop_price_offset(
        self,
        stop_price_offset: float,
    ) -> "OrderBuilder":
        """Set the stop price offset for the order.

        Args:
            stop_price_offset (float): The stop price offset for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["stop_price_offset"] = stop_price_offset
        return self

    def set_stop_type(self, stop_type: StopType) -> "OrderBuilder":
        """Set the stop type for the order.

        Args:
            stop_type (StopType): The stop type for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["stop_type"] = stop_type
        return self

    def set_price_link_basis(
        self,
        price_link_basis: PriceLinkBasis,
    ) -> "OrderBuilder":
        """Set the price link basis for the order.

        Args:
            price_link_basis (PriceLinkBasis): The price link basis for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["price_link_basis"] = price_link_basis
        return self

    def set_price_link_type(
        self,
        price_link_type: PriceLinkType,
    ) -> "OrderBuilder":
        """Set the price link type for the order.

        Args:
            price_link_type (PriceLinkType): The price link type for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["price_link_type"] = price_link_type
        return self

    def set_activation_price(
        self,
        activation_price: float,
    ) -> "OrderBuilder":
        """Set the activation price for the order.

        Args:
            activation_price (float): The activation price for the order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["activation_price"] = activation_price
        return self

    # TD Returns Error, No access to this functionality
    #  "Special Instructions are not allowed to be added to orders for accounts in this segment."
    def set_special_instruction(
        self,
        special_instruction: SpecialInstruction,
    ) -> "OrderBuilder":
        """Set the special instruction for the order.

        Args:
            special_instruction (SpecialInstruction): The special instruction for the
                order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["special_instruction"] = special_instruction
        return self

    # You need to enable this in your account settings
    #  https://invest.ameritrade.com/grid/p/site#r=jPage/cgi-bin/apps/u/DirectRouting
    #  Directy routing is not available for equity orders
    #  Direct routing is available for single-leg options orders
    def set_requested_destination(
        self,
        requested_destination: RequestedDestination,
    ) -> "OrderBuilder":
        """Set the requested destination for the order.

        Args:
            requested_destination (RequestedDestination): The requested destination for the
                order.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        self._order_dict["requested_destination"] = requested_destination
        return self

    # OrderLeg Related

    def add_leg(
        self,
        asset_type: AssetType,
        instruction: OrderInstruction,
        symbol: str,
        quantity: int,
        instrument: BaseInstrument | None = None,
    ) -> "OrderBuilder":
        """Add an order leg to the order.

        Args:
            asset_type (AssetType): The type of the asset for the order leg.
            instruction (Instruction): The instruction for the order leg.
            symbol (str): The symbol for the order leg.
            quantity (int): The quantity for the order leg.
            instrument (Instrument, optional): The instrument for the order leg. Defaults
                to None.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        if not instrument:
            instrument_cls = {
                AssetType.EQUITY: EquityInstrument,
                AssetType.OPTION: OptionInstrument,
                AssetType.INDEX: IndexInstrument,
                AssetType.MUTUAL_FUND: MutualFundInstrument,
                AssetType.CASH_EQUIVALENT: CashEquivalentInstrument,
                AssetType.FIXED_INCOME: FixedIncomeInstrument,
                AssetType.CURRENCY: CurrencyInstrument,
            }[asset_type]

            # TODO: Look into using InstrumentFactory here
            # this will only work for Instrument subclasses that have fields
            #  that don't require initialization
            #  (i.e. BaseInstrument only needs asset_type and symbol)
            instrument = instrument_cls(symbol=symbol)

        leg = OrderLeg(
            order_leg_type=asset_type,
            instrument=instrument,
            instruction=instruction,
            quantity=quantity,
        )
        self._legs.append(leg)
        return self

    def add_equity_leg(
        self, instruction: OrderInstruction, symbol: str, quantity: int
    ) -> "OrderBuilder":
        """Add an equity order leg to the order.

        Args:
            instruction (Instruction): The instruction for the order leg.
            symbol (str): The symbol for the order leg.
            quantity (int): The quantity for the order leg.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """
        return self.add_leg(
            asset_type=AssetType.EQUITY,
            instruction=instruction,
            symbol=symbol,
            quantity=quantity,
            instrument=EquityInstrument(symbol=symbol),
        )

    def add_option_leg(
        self,
        instruction: OrderInstruction,
        symbol: str,
        quantity: int,
        put_call: OptionSide | None = None,
        underlying_symbol: str | None = None,
        option_multiplier: int | None = None,
        option_deliverables: List[OptionDeliverable] | None = None,
    ) -> "OrderBuilder":
        """Add an option order leg to the order.
            Args:
        instruction (Instruction): The instruction for the order leg.
        symbol (str): The symbol for the order leg.
        quantity (int): The quantity for the order leg.
        option_type (OptionType, optional): The option type for the order leg.
            Defaults to None.
        put_call (OptionSide, optional): The option side for the order leg.
            Defaults to None.
        underlying_symbol (str, optional): The underlying symbol for the order leg.
            Defaults to None.
        option_multiplier (int, optional): The option multiplier for the order leg.
            Defaults to None.
        option_deliverables (List[OptionDeliverable], optional): The option deliverables
            for the order leg. Defaults to None.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """

        instrument = OptionInstrument(
            symbol=symbol,
            put_call=put_call,
            underlying_symbol=underlying_symbol,
            option_multiplier=option_multiplier,
            option_deliverables=option_deliverables,
        )
        return self.add_leg(
            asset_type=AssetType.OPTION,
            instruction=instruction,
            symbol=symbol,
            quantity=quantity,
            instrument=instrument,
        )

    # Other Instrument Types, not sure if these even work through api
    def add_index_leg(self):
        raise NotImplementedError

    def add_mutual_fund_leg(self):
        raise NotImplementedError

    def add_cash_equivalent_leg(self):
        raise NotImplementedError

    def add_fixed_income_leg(self):
        raise NotImplementedError

    # ChildOrderStrategies
    def add_child_order_strategy(self, child_order_strategy):
        """Add a child order strategy to the order.

        Args:
            child_order_strategy (Union[OrderBuilder, Order]): The child order strategy to add.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """

        if not isinstance(child_order_strategy, OrderBuilder) and not isinstance(
            child_order_strategy, Order
        ):
            raise ValueError("child_order_strategy must be OrderBuilder or Order")

        self._child_order_strategies.append(child_order_strategy)
        return self

    # ReplacingOrderCollection
    def add_replacing_order_collection(self, replacing_order_collection):
        """Add a replacing order collection to the order.

        Args:
            replacing_order_collection (Union[OrderBuilder, Order]): The replacing order
                collection to add.

        Returns:
            OrderBuilder: The OrderBuilder object.
        """

        if not isinstance(replacing_order_collection, OrderBuilder) and not isinstance(
            replacing_order_collection, Order
        ):
            raise ValueError("replacing_order_collection must be OrderBuilder or Order")

        self._replacing_order_collection.append(replacing_order_collection)
        return self

    def build(self) -> Order:
        """Build the order.

        Returns:
            Order: The built Order object.
        """
        self._order_dict["order_leg_collection"] = self._legs
        self._order_dict[
            "replacing_order_collection"
        ] = self._replacing_order_collection
        self._order_dict["child_order_strategies"] = self._child_order_strategies

        if len(self._order_dict["child_order_strategies"]) != 0:
            self._build_sub_orders(
                self._order_dict["child_order_strategies"], "child_order_strategies"
            )

        if len(self._order_dict["replacing_order_collection"]) != 0:
            self._build_sub_orders(
                self._order_dict["replacing_order_collection"],
                "replacing_order_collection",
            )

        return Order(**self._order_dict)

    def _build_sub_orders(self, sub_orders, sub_order_type):
        """Recursively build the sub orders.

        Args:
            sub_orders (List[Union[OrderBuilder, Order]]): The sub orders to build.
            sub_order_type (str): The type of the sub orders.
        """
        for i, sub_order in enumerate(sub_orders):
            if isinstance(sub_order, OrderBuilder):
                built_sub_order = sub_order.build()
                sub_orders[i] = built_sub_order
                if sub_order_type == "child_order_strategies":
                    self._build_sub_orders(
                        built_sub_order.child_order_strategies, "child_order_strategies"
                    )
                elif sub_order_type == "replacing_order_collection":
                    self._build_sub_orders(
                        built_sub_order.replacing_order_collection,
                        "replacing_order_collection",
                    )
            elif isinstance(sub_order, Order):
                continue
            else:
                raise ValueError("child order must be OrderBuilder or Order")
        return


def one_cancels_other(
    first_order: OrderBuilder | Order, second_order: OrderBuilder | Order
):
    """Create an OCO (One Cancels Other) order.
    Args:
    first_order (Union[OrderBuilder, Order]): The first order for the OCO.
    second_order (Union[OrderBuilder, Order]): The second order for the OCO.

    Returns:
        OrderBuilder: The OrderBuilder object.

    Example:
        >>> option_symbol = OptionSymbol("SPY", "053023", "P", "400").build()
        >>> option_limit_buy_order = option_buy_to_open_limit(
                option_symbol, 1, 0.10
            )  # DO NOT build here
        >>> option_limit_buy_order = option_buy_to_open_limit(option_symbol, 1, 0.05).build()

        >>> oco = one_cancels_other(option_limit_buy_order, option_limit_buy_order).build()
        >>> orders_service.place_order(account_number, oco)
    """
    return (
        OrderBuilder()
        .set_order_strategy_type(OrderStrategyType.OCO)
        .add_child_order_strategy(first_order)
        .add_child_order_strategy(second_order)
    )


def first_triggers_second(
    first_order: OrderBuilder, second_order: OrderBuilder | Order
):
    """Create a First Triggers Second order.
     Args:
         first_order (OrderBuilder): The first order for the First Triggers Second.
         second_order (Union[OrderBuilder, Order]): The second order for the First Triggers Second.

     Returns:
         OrderBuilder: The OrderBuilder object.

    Example:
        >>> option_symbol = OptionSymbol("SPY", "053023", "P", "400").build()
        >>> option_limit_buy_order = option_buy_to_open_limit(
                option_symbol, 1, 0.10
            )  # DO NOT build here
        >>> option_limit_sell_order = option_sell_to_close_limit(option_symbol, 1, 1.00).build()
        >>> fts = first_triggers_second(option_limit_buy_order, option_limit_sell_order).build()
        >>> orders_service.place_order(account_number, fts)
    """
    return first_order.set_order_strategy_type(
        OrderStrategyType.TRIGGER
    ).add_child_order_strategy(second_order)


def one_triggers_one_cancels_other(
    trigger_order: OrderBuilder,
    first_oco_order: OrderBuilder | Order,
    second_oco_order: OrderBuilder | Order,
):
    """Create a One Triggers One Cancels Other order.
    Args:
        trigger_order (OrderBuilder): The trigger order for the One Triggers One Cancels Other.
        first_oco_order (Union[OrderBuilder, Order]): The first order for the OCO.
        second_oco_order (Union[OrderBuilder, Order]): The second order for the OCO.

    Returns:
        OrderBuilder: The OrderBuilder object.

    Example:
        This strategy could be used when you want to take profit or limit loss after purchasing a stock or option.

        >>> option_symbol = OptionSymbol("SPY", "053023", "P", "400").build()
        >>> option_limit_buy_order = option_buy_to_open_limit(
                option_symbol, 1, 0.10
            )  # DO NOT build here
        >>> option_limit_sell_order = option_sell_to_close_limit(
                option_symbol, 1, 0.2
            )  # DO NOT build here
        >>> option_stop_limit_sell_to_close_order = (
                OrderBuilder()
                .set_session(Session.NORMAL)
                .set_duration(Duration.DAY)
                .set_order_type("LIMIT")
                .set_price(0.02)
                .set_order_strategy_type(OrderStrategyType.SINGLE)
                .add_option_leg(OrderInstruction.SELL_TO_CLOSE, option_symbol, 1)
                .build()  # Build Here
            )

        >>> otoco = one_triggers_one_cancels_other(
                option_limit_buy_order,
                option_limit_sell_order,
                option_stop_limit_sell_to_close_order,
            ).build()
        >>> orders_service.place_order(account_number, otoco)

    """
    return first_triggers_second(
        trigger_order, one_cancels_other(first_oco_order, second_oco_order)
    )
