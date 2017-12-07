# marketdataws.py
# Mohammad Usman
#
# A python wrapper for Gemini's market data websocket

from .basewebsocket import BaseWebSocket
from .debugly import typeassert
from collections import OrderedDict
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom
import os
import csv


class MarketDataWS(BaseWebSocket):
    """
    Market data is a public API that streams all the market data on a
    given symbol.
    """
    @typeassert(product_id=str, sandbox=bool)
    def __init__(self, product_id, sandbox=False):
        if sandbox:
            super().__init__(base_url='wss://api.sandbox.gemini.com/v1/marketdata/{}'
                             .format(product_id))
        else:
            super().__init__(base_url='wss://api.gemini.com/v1/marketdata/{}'
                             .format(product_id))

        self.product_id = product_id
        self.asks = OrderedDict()
        self.bids = OrderedDict()
        self.trades = []

    def on_message(self, msg):
        """
        Each msg will be a dict with the following keys: 'type',
        'eventId','socket_sequence', 'timestamp' and 'events'.

        'events' will be a list of dict's with each dict containing
        the following keys: 'type', 'tid', 'price', 'amount' and
        'makerSide'. If the first element of the list has type 'trade'
        then the method will append the trade to self.trades and add
        the event to either bids or asks depending on the 'makerSide'.
        """
        if msg['socket_sequence'] >= 1:
            event = msg['events'][0]
            if event['type'] == 'trade':
                self.trades.append(event)
                self.add(event['makerSide'], msg)

    @typeassert(side=str)
    def add(self, side, msg):
        """
        This method will create a custom order dict by extracting
        the appropriate information from the msg retrieved and then place the
        dict to either self.bids or self.asks depending on the 'makerSide'.

        Args:
            side(str): Either "buy" or "ask"
            msg(dict): Dict with keys: 'type','eventId','socket_sequence',
            'timestamp' and 'events'
        """
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

    @typeassert(price=str)
    def search_price(self, price):
        """
        Will return the all the trades on either asks or bids with the
        given price.

        Args:
            price(str): Must already be in self.asks or self.bids
        """
        if price in self.asks and price in self.bids:
            result = {'price': self.asks[price].extend(self.bids[price])}
        elif price in self.asks:
            result = {'price': self.asks[price]}
        elif price in self.bids:
            result = {'price': self.bids[price]}
        else:
            result = {'price': []}
        return result

    @typeassert(price=str, order=dict)
    def add_to_bids(self, price, order):
        """
        Allows the user to manually add an order to bids given it's
        an appropriate dict.

        Args:
            price(str): Must already be in self.asks or self.bids
            order(str): Dict with keys: 'eventId','socket_sequence','timestamp'
            and 'events'
        """
        if ('eventId' and 'timestamp' and 'price' and 'amount' and
                'makerSide') in order:
            if price in self.bids.keys():
                self.bids[price].append(order)
            else:
                self.bids[price] = [order]
        else:
            print("Orders must be a dict with the following keys: 'eventId', "
                  "'timestamp', 'price', 'amount' and 'makerSide'")

    @typeassert(price=str)
    def remove_from_bids(self, price):
        try:
            del self.bids[price]
        except KeyError as e:
            print('No order with price {} found'.format(price))

    @typeassert(price=str, order=dict)
    def add_to_asks(self, price, order):
        """
        Allows the user to manually asks an order to bids given it's
        an appropriate dict.

        Args:
            price(str): Must already be in self.asks or self.bids
            order(dict): Dict with keys: 'eventId','socket_sequence','timestamp'
            and 'events'
        """
        if ('eventId' and 'timestamp' and 'price' and 'amount' and
                'makerSide') in order:
            if price in self.asks.keys():
                self.asks[price].append(order)
            else:
                self.asks[price] = [order]
        else:
            print("Orders enter manually must be a dict with the following "
                  "keys: eventId, timestamp, price, amount and makerSide")

    @typeassert(price=str)
    def remove_from_asks(self, price):
        try:
            del self.asks[price]
        except KeyError as e:
            print('No order with price {} found'.format(price))

    @typeassert(dir=str, newline_selection=str)
    def export_to_csv(self, dir, newline_selection=''):
        """ Will export the trades recorded into a csv file.
        Note: directory for the file to be saved must be given as raw input.

        Args:
            dir(str): Must be in raw string
            newline_selection(str): Default value is ''
        """
        headers = ['type', 'tid', 'price', 'amount', 'makerSide']
        with open(os.path.join(r'{}'.format(dir), 'gemini_market_data.csv'),
                  'w',
                  newline=newline_selection) as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(self.trades)

    def _trades_to_xml(self):
        """
        Turn a list of dicts into XML.
        """
        parent_elem = Element('trades')
        for trade in self.trades:
            trade_elem = Element('trade')
            for key, val in trade.items():
                child = Element(key)
                child.text = str(val)
                trade_elem.append(child)
            parent_elem.append(trade_elem)
        return parent_elem

    @typeassert(dir=str)
    def export_to_xml(self, dir):
        """
        Will export the trades recorded into a xml file.
        Note: directory for the file to be saved must be given as raw input.
        Args:
            dir(str): Must be in raw string
        """
        rough_string = tostring(self._trades_to_xml(), 'utf-8')
        reparsed = minidom.parseString(rough_string).toprettyxml(indent="  ")
        with open(os.path.join(r'{}'.format(dir), 'gemini_market_data.xml'),
                  'w') as f:
            f.write(reparsed)
