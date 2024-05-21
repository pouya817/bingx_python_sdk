from base_request import base_request
from exeptions import BingxExceptionErrors
from config.config_dev import *
from types import *


class TradeData(base_request):
    def create_market_order(self, symbol: str, leverage: int, side: BingxOrderSide, type: BingxOrderType,
                            quantity: float, position_side: BingxPositionSide, **kwargs) -> dict:
        res_leverage = self.set_leverage(symbol=symbol, leverage=leverage, position_side=position_side)

        payload = {
            'symbol': symbol,
            'side': side.value,
            'type': type.value,
            'quantity': quantity,
            'leverage': leverage,
            'positionSide': position_side.value
        }

        if kwargs:
            payload.update(kwargs)

        res_order = self._request(method='POST', path=SET_BINGX_ORDER_URLS, query_params=payload)
        res_order = res_order.get('data').get('order')
        res_order.update(res_leverage.get('data'))
        return res_order

    def create_limit_order(self, symbol: str, leverage: int, side: BingxOrderSide, type: BingxOrderType,
                           quantity: float, price: float, position_side: BingxPositionSide, **kwargs) -> dict:

        res_leverage = self.set_leverage(symbol=symbol, leverage=leverage, position_side=position_side)

        payload = {
            'price': price,
            'symbol': symbol,
            'side': side.value,
            'type': type.value,
            'quantity': quantity,
            'leverage': leverage,
            'positionSide': position_side.value
        }

        if kwargs:
            payload.update(kwargs)

        res_order = self._request(method='POST', path=SET_BINGX_ORDER_URLS, query_params=payload)
        res_order = res_order.get('data').get('order')
        res_order.update(res_leverage.get('data'))
        return res_order

    def set_leverage(self, symbol: str, leverage: int, position_side: BingxPositionSide, **kwargs) -> dict:
        payload = {
            'symbol': symbol,
            'leverage': leverage,
            'side': position_side.value,
        }

        if kwargs:
            payload.update(kwargs)

        return self._request(method='POST', path=SET_BINGX_LEVERAGE_URLS, query_params=payload)

    def close_partially_future_orders(self, symbol: str, percent: int, side: BingxOrderSide,
                                      type: BingxOrderType, position_side: BingxPositionSide) -> dict:
        payload = {
            'symbol': symbol
        }
        quantity_order = self._request(method='GET', path=GET_BINGX_POSITION_URL, query_params=payload)

        data = quantity_order.get('data')

        if data and len(data) > 0:
            quantity = float(data[0]['availableAmt']) * percent
            payload = {
                'symbol': symbol,
                'side': side.value,
                'type': type.value,
                'quantity': quantity,
                'positionSide': position_side.value,
            }
            print(payload)
            response = self._request(method='POST', path=SET_BINGX_ORDER_URLS, query_params=payload)
            return response.get('data').get('order')
        else:
            raise BingxExceptionErrors(quantity_order)

    def cancel_future_orders(self, order_id: int, symbol: str):
        payload = {
            'orderId': order_id,
            'symbol': symbol
        }

        response = self._request(method='DELETE', path=CLOSE_BINGX_ORDER_URL, query_params=payload)

        if response.get('code') == 0:
            return response.get('data').get('order')
        return response

    def create_tp_sl(self, symbol: str, quantity: float, stop_price: float, side: BingxOrderSide,
                     position_side: BingxPositionSide, orders_type: OrdersType) -> dict:

        if orders_type == OrdersType.REQUESTED_TAKE_PROFIT:
            market_type = 'TAKE_PROFIT_MARKET'
        elif orders_type == OrdersType.REQUESTED_STOP_LOSS:
            market_type = 'STOP_MARKET'

        payload = {
            'symbol': symbol,
            'quantity': quantity,
            'stopPrice': stop_price,
            'side': side.value,
            'positionSide': position_side.value,
            'type': market_type,
        }
        response = self._request(method='POST', path=SET_BINGX_ORDER_URLS, query_params=payload)

        if response.get('code') == 0:
            return response.get('data').get('order')
        return response

    def get_future_order_details(self, symbol: str, order_id: str) -> dict:
        payload = {
            'symbol': symbol,
            'orderId': order_id
        }

        response = self._request(method='GET', path=GET_BINGX_OPEN_ORDERS_URL, query_params=payload)
        return response.get('data').get('order')