# private_client.py
# Mohammad Usman
#
# A python wrapper for Gemini's public API

from cached import Cached
import requests
import json
import hmac
import hashlib
import base64
import time


class PrivateClient(metaclass=Cached):
    def __init__(self, PUBLIC_API_KEY, PRIVATE_API_KEY):
        self._public_key = PUBLIC_API_KEY
        self._private_key = PRIVATE_API_KEY
        self._base_url = 'https://api.gemini.com/'

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
    def new_order(self, symbol, amount, price, side, options):
        payload = {
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'side': side,
            'options': options,
            'type': 'exchange limit'
        }
        return self.api_query('/v1/order/new', payload)

    def cancel_order(self, order_id):
        payload = {
            'order_id': order_id
        }
        return self.api_query('/v1/order/cancel', payload)

    def cancel_session_order(self):
        return self.api_query('/v1/order/cancel/session')

    def cancel_all_order(self):
        return self.api_query('/v1/order/cancel/all')

    # Order Status API
    def status_orders(self, order_id):
        payload = {
            'order_id': order_id
        }
        return self.api_query('/v1/order/status', payload)

    def active_orders(self):
        return self.api_query('/v1/orders')

    def get_past_trades(self, symbol, limit_trades=None):
        payload = {
            "symbol": symbol,
            "limit_trades": 500 if limit_trades is None else limit_trades
        }
        return self.api_query('/v1/mytrades', payload)

    def get_trade_volume(self):
        return self.api_query('/v1/tradevolume')
