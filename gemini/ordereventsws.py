# ordereventsws.py
# Mohammad Usman
#
# A python wrapper for Gemini's order events websocket
# This is a private endpoint and so requires a private and public keys

from .basewebsocket import BaseWebSocket
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
    def __init__(self, PUBLIC_API_KEY, PRIVATE_API_KEY):
        super().__init__(base_url='wss://api.sandbox.gemini.com/v1/order/events')
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
        order_types = ['subscription_ack', 'heartbeat', 'initial', 'accepted', 'rejected',
                       'booked', 'fill', 'cancelled', 'cancel_rejected', 'closed']
        for order_type in order_types:
            self.order_book[order_type] = list()

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
        return self.get_order_book()

    def remove_order(self, type, order_id):
        order_type = self.order_book[type]
        for index, order in enumerate(order_type):
            if order['order_id'] == order_id:
                pop_index = index
        try:
            del order_type[pop_index]
            print('Deleted order with order_id:{}'.format(order_id))
        except NameError as e:
            print('Order with order_id:{} does not exist '.format(order_id))

    def export_to_csv(self, dir, type, newline_selection=''):
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
            print("Type {} does not exist. Please select from: "
                  "'subscription_ack', 'heartbeat', 'initial', 'accepted', "
                  "'rejected', 'booked', 'fill', 'cancelled', "
                  "cancel_rejected' or 'closed'".format(type))

    def _trades_to_xml(self, type):
        ''' Turn a list of dicts into XML '''
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

    def export_to_xml(self, dir, type):
        if type in self.order_book.keys():
            rough_string = tostring(self._trades_to_xml(type), 'utf-8')
            reparsed = minidom.parseString(rough_string).toprettyxml(indent="  ")
            with open(os.path.join(r'{}'.format(dir), 'gemini_market_data.xml'),
                      'w') as f:
                f.write(reparsed)
                print('Successfully exported to xml')
        else:
            print("Type {} does not exist. Please select from: "
                  "'subscription_ack', 'heartbeat', 'initial', 'accepted', "
                  "'rejected', 'booked', 'fill', 'cancelled', "
                  "cancel_rejected' or 'closed'".format(type))
