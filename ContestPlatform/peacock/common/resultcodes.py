"""Descriptions of the result codes in Common API."""

from .._pyprotos.common_pb2 import (
    OK,
    SERVICE_UNAVAILABLE, REGISTER_DISABLED,
    INVALID_REQUEST, UNAUTHORIZED, UNSUBSCRIBED,
    TOO_MANY_ORDERS, TOO_MANY_REQUESTS,
    INVALID_ORDER, INVALID_BROKER_ID, INVALID_ORDER_ID,
    INVALID_TRADER_ID, INVALID_TRADER_NAME,
    INVALID_SYMBOL, INVALID_PRICE, INVALID_VOLUME,
    INVALID_SIDE, INVALID_POSITION,
    INSUFFICIENT_ASSETS, ACCOUNT_DISABLED, ON_MARGIN_CALL
)


def describe(result_code):
    """Returns a textual description of a result code."""
    return _MESSAGES.get(result_code) or 'unknown error'


_MESSAGES = {
    OK: 'OK',
    SERVICE_UNAVAILABLE: 'service is unavailable',
    REGISTER_DISABLED: 'registration is disabled',
    INVALID_REQUEST: 'invalid request',
    UNAUTHORIZED: 'unauthorized request',
    UNSUBSCRIBED: 'subscription needed',
    TOO_MANY_ORDERS: 'too many active orders',
    TOO_MANY_REQUESTS: 'too many requests',
    INVALID_ORDER: 'invalid order',
    INVALID_BROKER_ID: 'broker ID does not exist',
    INVALID_ORDER_ID: 'order ID does not exist',
    INVALID_TRADER_ID: 'trader ID does not exist',
    INVALID_TRADER_NAME: 'invalid trader name',
    INVALID_SYMBOL: 'instrument does not exist',
    INVALID_PRICE: 'invalid price',
    INVALID_VOLUME: 'invalid volume',
    INVALID_SIDE: 'invalid side',
    INVALID_POSITION: 'invalid position type',
    INSUFFICIENT_ASSETS: 'account has insufficient assets',
    ACCOUNT_DISABLED: 'account is disabled',
    ON_MARGIN_CALL: 'account is on margin call'
}
