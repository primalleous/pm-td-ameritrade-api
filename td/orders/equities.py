from td.enums.orders import (
    Duration,
    OrderInstruction,
    OrderStrategyType,
    OrderType,
    Session,
)
from td.orders.builder import OrderBuilder

# TODO: generate defaults from user_preferences and access in these functions
# TODO: have specific orders for types of stops (trailing, limit, etc.)

##########################################################################
# Buy orders


def equity_buy_market(symbol: str, quantity: int):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    buy market order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.MARKET)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.BUY, symbol, quantity)
    )


def equity_buy_limit(symbol, quantity, price):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    buy limit order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.LIMIT)
        .set_price(price)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.BUY, symbol, quantity)
    )


##########################################################################
# Sell orders


def equity_sell_market(symbol, quantity):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    sell market order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.MARKET)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.SELL, symbol, quantity)
    )


def equity_sell_limit(symbol, quantity, price):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    sell limit order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.LIMIT)
        .set_price(price)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.SELL, symbol, quantity)
    )


##########################################################################
# Short sell orders


def equity_sell_short_market(symbol, quantity):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    short sell market order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.MARKET)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.SELL_SHORT, symbol, quantity)
    )


def equity_sell_short_limit(symbol, quantity, price):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    short sell limit order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.LIMIT)
        .set_price(price)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.SELL_SHORT, symbol, quantity)
    )


##########################################################################
# Buy to cover orders


def equity_buy_to_cover_market(symbol, quantity):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    buy-to-cover market order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.MARKET)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.BUY_TO_COVER, symbol, quantity)
    )


def equity_buy_to_cover_limit(symbol, quantity, price):
    """
    Returns a pre-filled :class:`~td.orders.builder.OrderBuilder` for an equity
    buy-to-cover limit order.
    """

    return (
        OrderBuilder()
        .set_order_type(OrderType.LIMIT)
        .set_price(price)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_order_strategy_type(OrderStrategyType.SINGLE)
        .add_equity_leg(OrderInstruction.BUY_TO_COVER, symbol, quantity)
    )


"""
Substantial portions of this code were taken from

https://github.com/alexgolec/tda-api/blob/master/tda/orders/equities.py

MIT License

Copyright (c) 2020 Alexander Golec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
