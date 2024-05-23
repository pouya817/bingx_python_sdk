from base_request import base_request
from exeptions import BingxExceptionErrors
from config.config_dev import *
from types import *


class TradeData(base_request):
    def create_market_order(self, symbol: str, leverage: int, side: BingxOrderSide,
                            quantity: float, position_side: BingxPositionSide, **kwargs) -> dict:
        """
        Places a new order on BingX Swap.

        This function allows you to create various order types on BingX Swap.
        **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/)

        Args:
            symbol (str): The symbol of the contract to trade (e.g., "BTC-USDT").
            leverage (int): The leverage for the order (optional, default leverage applies).
            side (str): Order side, either "BUY" or "SELL".
            quantity (float): The order quantity.
            position_side (str): The position side, either "LONG" or "SHORT".
            kwargs (dict): Additional keyword arguments specific to the order type.
                Refer to the BingX API documentation for supported arguments.

        Returns:
            dict: A dictionary containing the API response.
                On success:
                {
                    "code": 0,
                    "msg": "",
                    "data": {
                        "order": {
                            "symbol": "BTC-USDT",
                            "orderId": 1735950529123455000,
                            "side": "BUY",
                            "positionSide": "LONG",
                            "type": "MARKET",
                            "clientOrderID": "",
                            "workingType": "MARK_PRICE"
                        }
                    }
                }
                On failure:
                {
                    "code": error code,
                    "msg": error message
                }
        """

        res_leverage = self.set_leverage(symbol=symbol, leverage=leverage, position_side=position_side)

        payload = {
            'symbol': symbol,
            'side': side.value,
            'type': 'MARKET',
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

    def create_limit_order(self, symbol: str, leverage: int, side: BingxOrderSide,
                           quantity: float, price: float, position_side: BingxPositionSide, **kwargs) -> dict:
        """
        Creates a limit order on BingX Swap.

        This function allows you to place a limit order on a specific contract at a desired price.

         **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/).

          **Note:** A limit order will only be executed if the market price reaches the specified price or a better
          price (lower for buys, higher for sells).

        Args:
            symbol (str): The symbol of the contract to trade (e.g., "BTC-USDT").
            leverage (int): The leverage for the order (optional, default leverage applies).
            side (str): Order side, either "BUY" or "SELL".
            quantity (float): The order quantity.
            price (float): The limit price for the order.
            position_side (str): The position side, either "LONG" or "SHORT".
            kwargs (dict, optional): Additional keyword arguments specific to the BingX API.
                Refer to the BingX API documentation for supported arguments.

        Returns:
            dict: A dictionary containing the API response.
                On success:
                    {
                        "code": 0,
                        "msg": "",
                        "data": {
                            "order": {
                                "symbol": "BTC-USDT",
                                "orderId": 1735950529123455000,
                                "side": "BUY",
                                "positionSide": "LONG",
                                "type": "LIMIT",
                                "clientOrderID": "",
                                "price": 30000.0  # Example limit price
                            }
                        }
                    }
                On failure:
                    {
                        "code": error code,
                        "msg": error message
                    }
        """

        res_leverage = self.set_leverage(symbol=symbol, leverage=leverage, position_side=position_side)

        payload = {
            'price': price,
            'symbol': symbol,
            'side': side.value,
            'type': 'LIMIT',
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
        """
        Sets leverage for a position on BingX Swap.

        This function allows you to adjust the leverage for an existing position on a specific contract.

         **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/)

          **Note:** Leverage amplifies your potential gains and losses, so use it cautiously.

        Args:
            symbol (str): The symbol of the contract for which to adjust leverage (e.g., "BTC-USDT").
            leverage (int): The new leverage level for the position.
            position_side (str, optional): The position side ("LONG" or "SHORT") for which to adjust leverage. Defaults to the current position side.
            kwargs (dict, optional): Additional keyword arguments specific to the BingX API.
                Refer to the BingX API documentation for supported arguments.

        Returns:
            dict: A dictionary containing the API response.
                On success:
                    {
                        "code": 0,
                        "msg": "",
                        "data": {
                            "leverage": 8,
                            "symbol": "ETH-USDT"
                        }
                    }
                On failure:
                    {
                        "code": error code,
                        "msg": error message
                    }
        """

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
        """
        Closes a partially filled future position on BingX Swap.

        This function allows you to close a portion of an existing position on a specific contract.
        **Note:** BingX API currently doesn't support partial closing by specifying a percentage.

        **Alternatives:**
          - Close the entire position by setting `quantity` to the full position size.
          - Consider using BingX's user interface or mobile app for partial closing functionalities.

        **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/)

        Args:
            symbol (str): The symbol of the contract for which to close a position (e.g., "BTC-USDT").
            quantity (float): The amount of the position to close.
            side (str): The closing side, either "BUY" or "SELL" depending on your initial position side.
            position_side (str, optional): The position side ("LONG" or "SHORT") to close from (defaults to the current position side).
            kwargs (dict, optional): Additional keyword arguments specific to the BingX API.
                Refer to the BingX documentation for supported arguments, but note that partial closing by percentage might not be supported.

        Returns:
            dict: A dictionary containing the API response.
                On success:
                    {
                        "code": 0,
                        "msg": "",
                        "timestamp": 0,
                        "data": {
                            "orderId": 1769649628749234200,
                            "positionId": "1769649551460794368",
                            "symbol": "BTC-USDT",
                            "side": "Ask",
                            "type": "Market",
                            "positionSide": "BOTH",
                            "origQty": "1.0000"
                        }
                    }
                On failure:
                    {
                        "code": error code,
                        "msg": error message
                    }
        """

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
        """
        Cancels a pending future order on BingX Swap.

        This function allows you to cancel an order that has not yet been filled.

         **Once an order is filled, it cannot be canceled.**

          **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/)

        Args:
            order_id (str): The unique identifier (ID) of the order to be canceled.

        Returns:
            dict: A dictionary containing the API response.
                On success:
                    {
                        "code": 0,
                        "msg": "",
                        "timestamp": 0,
                        "data": {
                            "orderId": 1769649628749234200,
                            "positionId": "1769649551460794368",
                            "symbol": "BTC-USDT",
                            "side": "Ask",
                            "type": "Market",
                            "positionSide": "BOTH",
                            "origQty": "1.0000"
                        }
                    }
                On failure:
                    {
                        "code": error code,
                        "msg": error message
                    }
        """

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
        """
        Creates Take Profit (TP) and Stop Loss (SL) orders on BingX Swap.

        This function allows you to simultaneously set both a Take Profit (TP) and a Stop Loss (SL) order for an existing position on a specific contract.



         **Important:** Refer to the BingX API documentation [BingX API Docs](https://bingx-api.github.io/docs/)

          **Note:** These conditional orders help manage your risk and potential profit by automatically exiting the position when the market price reaches your specified levels.

        Args:
            symbol (str): The symbol of the contract for which to create TP/SL orders (e.g., "BTC-USDT").
            quantity (float): The quantity of the existing position for which TP/SL orders apply.
            stop_price (float): The price at which to trigger the Stop Loss order.
            side (str): The position side ("LONG" or "SHORT") for which to create TP/SL orders.
            position_side (str, optional): The position side ("LONG" or "SHORT") to target with the TP/SL orders. Defaults to the current position side.
            orders_type (str, optional): The type of TP/SL orders to create. Currently supported options depend on the BingX API version you're using. Refer to the documentation for valid choices.

        Returns:
            dict: A dictionary containing the API response.
                On success: (Structure may vary depending on BingX API version)
                    {
                        "code": 0,  # May differ depending on success/failure
                        "msg": "",  # May differ depending on success/failure
                        "data": {
                            # Details may vary, but might include order IDs or confirmation messages
                        }
                    }
                On failure:
                    {
                        "code": error code,
                        "msg": error message
                    }
        """

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