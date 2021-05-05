# private_client.py
# Mohammad Usman
#
# A python wrapper for Gemini's public API

from .public_client import PublicClient
from .debugly import typeassert
import requests
import json
import hmac
import hashlib
import base64
import time


class PrivateClient(PublicClient):
    @typeassert(PUBLIC_API_KEY=str, PRIVATE_API_KEY=str, sandbox=bool)
    def __init__(self, PUBLIC_API_KEY, PRIVATE_API_KEY, sandbox=False):
        super().__init__(sandbox)
        self._public_key = PUBLIC_API_KEY
        self._private_key = PRIVATE_API_KEY
        if sandbox:
            self._base_url = 'https://api.sandbox.gemini.com'
        else:
            self._base_url = 'https://api.gemini.com'

    @typeassert(method=str, payload=dict)
    def api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        request_url = self._base_url + method

        payload['request'] = method
        payload['nonce'] = int(time.time() * 1000)
        b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8'))
        signature = hmac.new(self._private_key.encode('utf-8'), b64_payload, hashlib.sha384).hexdigest()

        headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': self._public_key,
            'X-GEMINI-PAYLOAD': b64_payload,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': "no-cache"
        }

        r = requests.post(request_url, headers=headers)
        return r.json()

    # Order Placement API
    @typeassert(symbol=str, amount=str, price=str, side=str, options=list)
    def new_order(self, symbol, amount, price, side, options=["immediate-or-cancel"]):
        """
        This endpoint is used for the creation of a new order.
        Requires you to provide the symbol, amount, price, side and options.
        Options is an array and should include on the following:
        "maker-or-cancel","immediate-or-cancel", auction-only"
        So far Gemini only supports "type" as "exchange limit".

        Args:
            product_id(str): Can be any value in self.symbols()
            amount(str): The amount of currency you want to buy.
            price(str): The price at which you want to buy the currency/
            side(str): Either "buy" or "ask"
            options(list): Currently, can only be ["immediate-or-cancel"]

        Returns:
            dict: These are the same fields returned by order/status
            example: {
                'order_id': '86403510',
                'id': '86403510',
                'symbol': 'btcusd',
                'exchange': 'gemini',
                'avg_execution_price': '0.00',
                'side': 'buy',
                'type': 'exchange limit',
                'timestamp': '1510403257',
                'timestampms': 1510403257453,
                'is_live': True,
                'is_cancelled': False,
                'is_hidden': False,
                'was_forced': False,
                'executed_amount': '0',
                'remaining_amount': '0.02',
                'options': ['maker-or-cancel'],
                'price': '6400.28',
                'original_amount': '0.02'
            }
        """
        payload = {
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'side': side,
            'options': options,
            'type': 'exchange limit'
        }
        return self.api_query('/v1/order/new', payload)

    @typeassert(order_id=str)
    def cancel_order(self, order_id):
        """
        Used for the cancellation of an order via it's ID. This ID is provided
        when the user creates a new order.

        Args:
            order_id(str): Order must be not be filled

        Results:
            dict: These are the same fields returned by order/cancel
            example: {
                'order_id': '86403510',
                'id': '86403510',
                'symbol': 'btcusd',
                'exchange': 'gemini',
                'avg_execution_price': '0.00',
                'side': 'buy',
                'type': 'exchange limit',
                'timestamp': '1510403257',
                'timestampms': 1510403257453,
                'is_live': False,
                'is_cancelled': True,
                'is_hidden': False,
                'was_forced': False,
                'executed_amount': '0',
                'remaining_amount': '0.02',
                'options': ['maker-or-cancel'],
                'price': '6400.28',
                'original_amount': '0.02'
            }
        """
        payload = {
            'order_id': order_id
        }
        return self.api_query('/v1/order/cancel', payload)

    def cancel_session_orders(self):
        """
        Used for the cancellation of all orders in a session.

        Results:
            dict: The response will be a dict with two keys: "results"
            and "details"
            example: {
                'result': 'ok',
                'details': {
                    'cancelledOrders': [86403350, 86403386, 86403503, 86403612],
                    'cancelRejects': []
                }
            }
        """
        return self.api_query('/v1/order/cancel/session')

    def cancel_all_orders(self):
        """
        Cancels all current orders open.

        Results: Same as cancel_session_order
        """
        return self.api_query('/v1/order/cancel/all')

    # Order Status API
    @typeassert(order_id=str)
    def status_of_order(self, order_id):
        """
        Get's the status of an order.
        Note: the API used to access this endpoint must have the "trader"
        functionality assigned to it.

        Args:
            order_id(str): Order can be in any state

        Results:
            dict: Returns the order_id, id, symbol, exchange, avh_execution_price,
            side, type, timestamp, timestampms, is_live, is_cancelled, is_hidden,
            was_forced, exucuted_amount, remaining_amount, options, price and
            original_amount
            example: {
                'order_id': '44375901',
                'id': '44375901',
                'symbol': 'btcusd',
                'exchange': 'gemini',
                'avg_execution_price': '400.00',
                'side': 'buy',
                'type': 'exchange limit',
                'timestamp': '1494870642',
                'timestampms': 1494870642156,
                'is_live': False,
                'is_cancelled': False,
                'is_hidden': False,
                'was_forced': False,
                'executed_amount': '3',
                'remaining_amount': '0',
                'options': [],
                'price': '400.00',
                'original_amount': '3'
            }
        """
        payload = {
            'order_id': order_id
        }
        return self.api_query('/v1/order/status', payload)

    def active_orders(self):
        """
        Returns all the active_orders associated with the API.

        Results:
            array: An array of the results of /order/status for all your live orders.
            Each entry is similar to status_of_order
        """
        return self.api_query('/v1/orders')

    @typeassert(symbol=str, limit_trades=int)
    def get_past_trades(self, symbol, limit_trades=None):
        """
        Returns all the past trades associated with the API.
        Providing a limit_trade is optional.

        Args:
            symbols(str): Can be any value in self.symbols()
            limit_trades(int): Default value is 500

        Results:
            array: An array of of dicts of the past trades
        """
        payload = {
            "symbol": symbol,
            "limit_trades": 500 if limit_trades is None else limit_trades
        }
        return self.api_query('/v1/mytrades', payload)

    def get_trade_volume(self):
        """
        Returns the trade volume associated with the API for the past
        30 days.

        Results:
            array: An array of dicts of the past trades
        """
        return self.api_query('/v1/tradevolume')

    # Fund Management API
    def get_balance(self):
        """
        This will show the available balances in the supported currencies.

        Results:
            array: An array of elements, with one block per currency
            example: [
                {
                    'type': 'exchange',
                    'currency': 'BTC',
                    'amount': '19.17997442',
                    'available': '19.17997442',
                    'availableForWithdrawal': '19.17997442'
                },
                {
                    'type': 'exchange',
                    'currency': 'USD',
                    'amount': '4831517.78',
                    'available': '4831389.45',
                    'availableForWithdrawal': '4831389.45'
                }
            ]
        """
        return self.api_query('/v1/balances')

    @typeassert(currency=str, label=str)
    def create_deposit_address(self, currency, label=None):
        """
        This will create a new cryptocurrency deposit address with an optional label.

        Args:
            currency(str): Can either be btc or eth
            label(str): Optional

        Results:
            dict: A dict of the following fields: currency, address, label
        """
        if label:
            payload = {
                "label": label
            }
        else:
            payload = {}
        return self.api_query('/v1/deposit/{}/newAddress'.format(currency), payload)

    @typeassert(currency=str, address=str, amount=str)
    def withdraw_to_address(self, currency, address, amount):
        """
        This will allow you to withdraw currency from the address
        provided.
        Note: Before you can withdraw cryptocurrency funds to a whitelisted
        address, you need three things: cryptocurrency address whitelists
        needs to be enabled for your account, the address you want to withdraw
        funds to needs to already be on that whitelist and an API key with the
        Fund Manager role added.

        Args:
            current(str): Can either be btc or eth
            address(str): The address you want the money to be sent to
            amount(str): Amount you want to transfer

        Results:
            dict: A dict of the following fields: destination, amount, txHash
        """
        payload = {
            "address": address,
            "amount": amount
        }
        return self.api_query('/v1/withdraw/{}'.format(currency), payload)

    # Transfers API
    @typeassert(limit_transfers=int, show_completed_deposit_advances=bool)
    def get_past_transfers(self, limit_transfers=None, show_completed_deposit_advances=False):
        """
        Returns all the past transfers associated with the API.
        Providing a limit_trade is optional.
        Whether to display completed deposit advances. False by default. Must be set True to activate. Defaults to False.

        Args:
            limit_trades(int): Default value is 500
            show_completed_deposit_advances(bool): Default value is False

        Results:
            array: An array of of dicts of the past transfers
        """
        payload = {
            "limit_transfers": 500 if limit_transfers is None else limit_transfers,
            "show_completed_deposit_advances": show_completed_deposit_advances
        }
        return self.api_query('/v1/transfers', payload)

    # HeartBeat API
    def revive_hearbeat(self):
        """
        Revive the heartbeat if 'heartbeat' is selected for the API.
        """
        return self.api_query('/v1/heartbeat')
