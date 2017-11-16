# marketdataws.py
# Mohammad Usman
#
# A python wrapper for Gemini's market data websocket

from .basewebsocket import BaseWebSocket
from collections import OrderedDict
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom
import os
import csv


class MarketDataWS(BaseWebSocket):
    def __init__(self, product_id):
        super().__init__(base_url='wss://api.gemini.com/v1/marketdata/{}'
                         .format(product_id))
        self.product_id = product_id
        self.asks = OrderedDict()
        self.bids = OrderedDict()
        self.trades = []

    def on_message(self, msg):
        if msg['socket_sequence'] >= 1:
            event = msg['events'][0]
            if event['type'] == 'trade':
                self.trades.append(event)
                self.add(event['makerSide'], msg)

    def add(self, side, msg):
        trade_event = msg['events'][0]
        order = {
            'eventId': msg['eventId'],
            'timestamp': msg['timestamp'],
            'price': trade_event['price'],
            'amount': trade_event['amount'],
            'makerSide': trade_event['makerSide']
        }
        if trade_event['makerSide'] == 'bid':
            self.add_to_bids(trade_event['price'], order)
        else:
            self.add_to_asks(trade_event['price'], order)

    def get_market_book(self):
        result = {
            'asks': self.asks,
            'bids': self.bids
        }
        return result

    def reset_market_book(self):
        self.asks, self.bids = OrderedDict(), OrderedDict()
        print('Market book reset to empty')

    def search_price(self, price):
        result = {'price': self.asks[price].extend(self.bids[price])}
        return result

    def add_to_bids(self, price, order):
        if price in self.bids.keys():
            self.bids[price].append(order)
        else:
            self.bids[price] = [order]

    def remove_from_bids(self, price):
        del self.bids[price]

    def add_to_asks(self, price, order):
        if price in self.asks.keys():
            self.asks[price].append(order)
        else:
            self.asks[price] = [order]

    def remove_from_asks(self, price):
        del self.asks[price]

    def export_to_csv(self, dir, newline_selection=''):
        headers = ['type', 'tid', 'price', 'amount', 'makerSide']
        with open(os.path.join(r'{}'.format(dir), 'gemini.csv'),
                  'w',
                  newline=newline_selection) as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(self.trades)

    def _trades_to_xml(self):
        ''' Turn a list of dicts into XML '''
        parent_elem = Element('trades')
        for trade in self.trades:
            trade_elem = Element('trade')
            for key, val in trade.items():
                child = Element(key)
                child.text = str(val)
                trade_elem.append(child)
            parent_elem.append(trade_elem)
        return parent_elem

    def export_to_xml(self, dir):
        rough_string = tostring(self._trades_to_xml(), 'utf-8')
        reparsed = minidom.parseString(rough_string).toprettyxml(indent="  ")
        with open(os.path.join(r'{}'.format(dir), 'gemini.xml'), 'w') as f:
            f.write(reparsed)
