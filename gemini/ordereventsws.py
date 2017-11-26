# ordereventsws.py
# Mohammad Usman
#
# A python wrapper for Gemini's order events websocket
# This is a private endpoint and so requires a private and public keys

from .basewebsocket import BaseWebSocket
from websocket import create_connection
from collections import OrderedDict
import json
import hmac
import hashlib
import base64
import time


class OrderEventsWS(BaseWebSocket):
    def __init__(self, PUBLIC_API_KEY, PRIVATE_API_KEY):
        super().__init__(base_url='wss://api.sandbox.gemini.com/v1/order/events')
        self._public_key = PUBLIC_API_KEY
        self._private_key = PRIVATE_API_KEY
        self.hearbeats = []
        self.initial_orders = []
        self.accepted_orders = []
        self.rejected_orders = []
        self.booked_orders = []
        self.filled_orders = []
        self.cancelled_orders = []
        self.cancel_rejected_orders = []
        self.closed_orders = []

    def api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        payload['request'] = method
        payload['nonce'] = int(time.time() * 1000)
        b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8'))
        signature = hmac.new(self._private_key.encode('utf-8'), b64_payload, hashlib.sha384).hexdigest()

        headers = {
            'X-GEMINI-APIKEY': self._public_key,
            'X-GEMINI-PAYLOAD': b64_payload.decode('utf-8'),
            'X-GEMINI-SIGNATURE': signature
        }
        return headers

    def _connect(self):
        self.ws = create_connection('wss://api.sandbox.gemini.com/v1/order/events',
                                    header=self.api_query('/v1/order/events'),
                                    skip_utf8_validation=True)

    def on_message(self, msg):
        if msg['type'] == 'heartbeat':
            self.heartbeats.append(msg)
        else:
            for order in msg:
                if order['type'] == 'initial':
                    self.initial_orders.append(order)
                elif order['type'] == 'accepted':
                    self.accepted_orders.append(order)
                elif order['type'] == 'rejected':
                    self.rejected_orders.append(order)
                elif order['type'] == 'booked':
                    self.booked_orders.append(order)
                elif order['type'] == 'fill':
                    self.filled_orders.append(order)
                elif order['type'] == 'cancelled':
                    self.cancelled_orders.append(order)
                elif order['type'] == 'cancel_rejected':
                    self.cancel_rejected_orders.append(order)
                else:
                    self.closed_orders.append(order)

    def get_order_book(self):
        return {
            'initial_orders': self.initial_orders,
            'accepted_orders': self.accepted_orders,
            'rejected_orders': self.rejected_orders,
            'booked_orders': self.booked_orders,
            'filled_orders': self.filled_orders,
            'cancelled_orders': self.cancelled_orders,
            'cancel_rejected_orders': self.cancel_rejected_orders,
            'closed_orders': self.closed_orders
        }

    def remove_order(self, type, order_id):
        for index, order in enumerate(self.get_order_book()[type]):
            if order['order_id'] == 'order_id':
                self._pop = index
        del self.order_books()[type][self._pop]
