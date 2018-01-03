# order_book.py
# Sebastian Quilter
#
# A python wrapper for Gemini which keeps an updated order book

import time

from .basewebsocket import BaseWebSocket
from .debugly import typeassert

class GeminiOrderBook(BaseWebSocket):
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
        self.asks = {}
        self.bids = {}

    def on_message(self, msg):
        if msg['socket_sequence'] >= 1:
            for event in msg['events']:
                if event['type'] == 'change':
                    price = float(event['price'])
                    remaining = float(event['remaining'])
                    if(event['side'] == 'ask'):
                        if(remaining == 0.0 and price in self.asks):
                            self.asks.pop(price)
                        elif(remaining != 0.0):
                            self.asks[price] = remaining
                    elif(event['side'] == 'bid'):
                        if(remaining == 0.0 and price in self.bids):
                            self.bids.pop(price)
                        elif(remaining != 0.0):
                            self.bids[price] = remaining

    def get_ask(self):
        return min(self.asks.keys())

    def get_bid(self):
        return max(self.bids.keys())

    def get_market_book(self):
        result = {
            'asks': self.asks,
            'bids': self.bids
        }
        return result

    def reset_market_book(self):
        self.asks, self.bids = {}, {}
        print('Market book reset to empty')

