from enum import Enum


class OrdersType(Enum):
    OPENED_TAKE_PROFIT = 'opened_take_profit'
    REQUESTED_TAKE_PROFIT = 'requested_take_profit'
    CANCELED_TAKE_PROFIT = 'canceled_take_profit'
    REQUESTED_CANCEL_TAKE_PROFIT = 'requested_cancel_take_profit'
    TRIGGERED_TAKE_PROFIT = 'triggered_take_profit'
    OPENED_STOP_LOSS = 'opened_stop_loss'
    REQUESTED_STOP_LOSS = 'requested_stop_loss'
    CANCELED_STOP_LOSS = 'canceled_stop_loss'
    REQUESTED_CANCEL_STOP_LOSS = 'requested_cancel_stop_loss'
    TRIGGERED_STOP_LOSS = 'triggered_stop_loss'
    OPEN_ORDER = 'open_order'
    REQUESTED_OPEN_ORDER = 'requested_open_order'
    PARTIAL_CLOSE_ORDER = 'partial_close_order'
    REQUESTED_PARTIAL_CLOSE_ORDER = 'requested_partial_close_order'
    OPENED_CLOSE_ORDER = 'opened_close_order'
    REQUESTED_CLOSE_ORDER = 'requested_close_order'
    URGENT_CLOSE_ORDER = 'urgent_close_order'
    REQUESTED_URGENT_CLOSE_ORDER = 'requested_urgent_close_order'

class BingxOrderType(Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'


class BingxOrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class BingxPositionSide(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'
