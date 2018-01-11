# ordereventsws.py
# Mohammad Usman
#
# A python wrapper for Gemini's order events websocket
# This is a private endpoint and so requires a private and public keys

from .basewebsocket import BaseWebSocket
from .debugly import typeassert
from websocket import create_connection
from collections import OrderedDict
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom
import os
import csv
import json
import hmac
import hashlib
import base64
import time


class OrderEventsWS(BaseWebSocket):
    @typeassert(PUBLIC_API_KEY=str, PRIVATE_API_KEY=str, sandbox=bool)
    def __init__(self, PUBLIC_API_KEY, PRIVATE_API_KEY, sandbox=False):
        if sandbox:
            super().__init__(base_url='wss://api.sandbox.gemini.com/v1/order/events')
        else:
            super().__init__(base_url='wss://api.gemini.com/v1/order/events')
        self._public_key = PUBLIC_API_KEY
        self._private_key = PRIVATE_API_KEY
        self.order_book = OrderedDict()
        self._reset_order_book()

    @property
    def get_order_types(self):
        print("Order types are: subscription_ack', 'heartbeat', 'initial', "
              "'accepted','rejected', 'booked', 'fill', 'cancelled', "
              "cancel_rejected' or 'closed'")

    def _reset_order_book(self):
        """
        Will create a dict with all the following msg types to be received
        by the websocket.
        """
        order_types = ['subscription_ack', 'heartbeat', 'initial', 'accepted',
                       'rejected', 'booked', 'fill', 'cancelled',
                       'cancel_rejected', 'closed']
        for order_type in order_types:
            self.order_book[order_type] = list()

    @typeassert(method=str, payload=dict)
    def api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        payload['request'] = method
        payload['nonce'] = int(time.time() * 1000)
        b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8'))
        signature = hmac.new(self._private_key.encode('utf-8'),
                             b64_payload, hashlib.sha384).hexdigest()

        headers = {
            'X-GEMINI-APIKEY': self._public_key,
            'X-GEMINI-PAYLOAD': b64_payload.decode('utf-8'),
            'X-GEMINI-SIGNATURE': signature
        }
        return headers

    def _connect(self):
        self.ws = create_connection(self.base_url,
                                    header=self.api_query('/v1/order/events'),
                                    skip_utf8_validation=True)

    def on_message(self, msg):
        """
        Each msg will either be a list or a dict. The first msg to be
        recieved with be a subscription acknowledgement with the following
        keys: 'type', 'accountId', 'subscriptionId', 'symbolFilter',
        'apiSessionFilter' and 'eventTypeFilter'.

        Any messages recieved further will be of two types: either a heartbeat
        or a list of events. Gemini will send a hearbeat every 5 seconds and
        recommends the user store all hearbeats. Each list of events will have
        the following keys: 'type', 'socket_sequence', 'order_id', 'event_id',
        'api_session', 'client_order_id', 'symbol', 'side', 'behavior',
        'order_type', 'timestamp', 'timestampms', 'is_live', 'is_cancelled',
        'is_hidden', 'avg_execution_price', 'executed_amount',
        'remaining_amount', 'original_amount', 'price' and 'total_spend'. This
        method will check the type of any orders and assign them to their
        appropriate keys within self.order_book.
        """
        if isinstance(msg, list):
            for order in msg:
                self.order_book[order['type']].append(order)
        elif msg['type'] == 'subscription_ack':
            self.order_book['subscription_ack'].append(msg)
        elif msg['type'] == 'heartbeat':
            self.order_book['heartbeat'].append(msg)
        else:
            pass

    def get_order_book(self):
        return self.order_book

    def reset_order_book(self):
        self._reset_order_book()
        print('Order book reset to empty')

    @typeassert(type=str, order_id=str)
    def remove_order(self, type, order_id):
        """
        Will remove a order given a type within self.order_book and the
        orders id number.

        Args:
            type(str): Can be any value in self.get_order_types
            order_id(str): Must already be in self.order_book[type]
        """
        order_type = self.order_book[type]
        for index, order in enumerate(order_type):
            if order['order_id'] == order_id:
                pop_index = index
        try:
            del order_type[pop_index]
            print('Deleted order with order_id:{}'.format(order_id))
        except NameError as e:
            print('Order with order_id:{} does not exist '.format(order_id))

    @typeassert(dir=str, type=str, newline_selection=str)
    def export_to_csv(self, dir, type, newline_selection=''):
        """
        Will export the orders of a specific type to a csv format. If the
        type given is not in self.order_book then it'll print an error message
        with instructions of the appropriate types to be entered.
        Note: directory for the file to be saved must be given as raw input

        Args:
            dir(str): Must be in raw string
            type(str): Can be any valie in self.get_order_types
            newline_selection(str): Default value is ''
        """
        if type in self.order_book.keys():
            order_type = self.order_book[type]
            if len(order_type) >= 1:
                headers = order_type[0].keys()
                with open(os.path.join(r'{}'.format(dir), 'gemini_order_events.csv'),
                          'w',
                          newline=newline_selection) as f:
                    f_csv = csv.DictWriter(f, headers)
                    f_csv.writeheader()
                    f_csv.writerows(order_type)
                    print('Successfully exported to csv')
            else:
                print('No order with type {} recorded'.format(type))
        else:
            print("Type {} does not exist. Please select from: "
                  "'subscription_ack', 'heartbeat', 'initial', 'accepted', "
                  "'rejected', 'booked', 'fill', 'cancelled', "
                  "cancel_rejected' or 'closed'".format(type))

    def _trades_to_xml(self, type):
        """
        Turn a list of dicts into XML.
        """
        order_type = self.order_book[type]
        parent_elem = Element(type + 'orders')
        for trade in order_type:
            trade_elem = Element(type)
            for key, val in trade.items():
                child = Element(key)
                child.text = str(val)
                trade_elem.append(child)
        parent_elem.append(trade_elem)
        return parent_elem

    @typeassert(dir=str, type=str)
    def export_to_xml(self, dir, type):
        """
        Will export the orders of a specific type to a xml format. If the
        type given is not in self.order_book then it'll print an error message
        with instructions of the appropriate types to be entered.
        Note: directory for the file to be saved must be given as raw input.

        Args:
            dir(str): Must be in raw string
            type(str): Can be any valie in self.get_order_types
        """
        if type in self.order_book.keys():
            if len(self.order_book[type]) >= 1:
                rough_string = tostring(self._trades_to_xml(type), 'utf-8')
                reparsed = minidom.parseString(rough_string).toprettyxml(indent="  ")
                with open(os.path.join(r'{}'.format(dir), 'gemini_order_events.xml'),
                          'w') as f:
                    f.write(reparsed)
                    print('Successfully exported to xml')
            else:
                print('No order with type {} recorded'.format(type))
        else:
            print("Type {} does not exist. Please select from: "
                  "'subscription_ack', 'heartbeat', 'initial', 'accepted', "
                  "'rejected', 'booked', 'fill', 'cancelled', "
                  "cancel_rejected' or 'closed'".format(type))
