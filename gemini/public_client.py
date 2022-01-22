# public_client.py
# Mohammad Usman
#
# A python wrapper for Gemini's public API

from .cached import Cached
from .debugly import typeassert
import requests
import time
import datetime


class PublicClient(metaclass=Cached):
    @typeassert(sandbox=bool)
    def __init__(self, sandbox=False):
        if sandbox:
            self.public_base_url = 'https://api.sandbox.gemini.com/v1'
        else:
            self.public_base_url = 'https://api.gemini.com/v1'

    def symbols(self):
        """
        This endpoint retrieves all available symbols for trading.

        Returns:
            list: Will output an array of supported symbols
            example: ['btcusd', 'ethbtc', 'ethusd']
        """
        r = requests.get(self.public_base_url + '/symbols')
        return r.json()

    @typeassert(product_id=str)
    def symbol_details(self, product_id):
        """
        This endpoint retrieves extra detail on supported symbols, such as
        minimum order size, tick size, quote increment and more.

        Args:
            product_id(str): Can be any value in self.symbols()

        Returns:
            dict:tick_size, quote_increment, min_order_size, status and wrap_enabled
            example: {
                "symbol":"BTCUSD",
                "base_currency":"BTC",
                "quote_currency":"USD",
                "tick_size":1e-08,
                "quote_increment":0.01,
                "min_order_size":"0.00001",
                "status":"open",
                "wrap_enabled":false
            }
        """
        r = requests.get(self.public_base_url
                         + '/symbols/details/' + product_id)
        return r.json()

    @typeassert(product_id=str)
    def get_ticker(self, product_id):
        """
        This endpoint retrieves information about recent trading
        activity for the symbol.

        Args:
            product_id(str): Can be any value in self.symbols()

        Returns:
                dict: the latest bid, ask, last price qouted and the volume
                example: {
                    'bid': '6398.99',
                    'ask': '6399.00',
                    'volume': {
                                'BTC': '15122.8052525982',
                                'USD': '100216283.474911855175',
                                'timestamp': 1510407900000
                            },
                    'last': '6398.99'
                }
        """
        r = requests.get(self.public_base_url + '/pubticker/' + product_id)
        return r.json()

    @typeassert(product_id=str)
    def get_current_order_book(self, product_id):
        """
        This endpoint retreives information about the recents orders.

        Args:
            product_id(str): Can be any value in self.symbols()

        Returns:
            dict: This will return the current order book, as two arrays,
            one of bids, and one of asks
            example:{
              'bids': [ /* bids look like asks */ ],
              'asks': [
                {
                    'price': '6400.00',
                    'amount': '3.04177064',
                    'timestamp': '1510408074'
                },
                ...
              ]
            }
        """
        r = requests.get(self.public_base_url + '/book/' + product_id)
        return r.json()

    @typeassert(product_id=str, since=str)
    def get_trade_history(self, product_id, since=None):
        """
        This endpoint will return the trades that have executed since the
        specified timestamp. Timestamps are either seconds or milliseconds
        since the epoch (1970-01-01).

        Args:
            product_id(str): Can be any value in self.symbols()
            since(str): Must be in DD/MM/YYYY format

        Returns:
            list: Will return at most 500 records
            example:[
              {
                'timestamp': 1510408136,
                'timestampms': 1510408136595,
                'tid': 2199657585,
                'price': '6399.02',
                'amount': '0.03906848',
                'exchange': 'gemini',
                'type': 'buy'
              },
              ...
            ]
        """
        if since is None:
            r = requests.get(self.public_base_url + '/trades/' + product_id)
        else:
            self.timestamp = time.mktime(datetime.datetime.strptime(since,
                                                                    "%d/%m/%Y").timetuple())
            r = requests.get(self.public_base_url + '/trades/{}?since={}'.format(
                product_id, int(self.timestamp)))
        return r.json()

    @typeassert(product_id=str, since=str)
    def get_auction_history(self, product_id, since=None):
        """
        This will return the auction events, optionally including
        publications of indicative prices, since the specific timestamp.

        Args:
            product_id(str): Can be any value in self.symbols()
            since(str): must be in DD/MM/YYYY format

        Returns:
            list: Will return at most 500 records if date is provided.
            Otherwise it'll output a dictionary for the current auction
            example:[
                {
                    'last_auction_price': '6580.01',
                    'last_auction_quantity': '0.01515964',
                    'last_highest_bid_price': '6580.00',
                    'last_lowest_ask_price': '6580.01',
                    'next_update_ms': 1510433400000,
                    'next_auction_ms': 1510434000000,
                    'last_auction_eid': 2199289141
                },
                ...
            ]
        """
        if since is None:
            r = requests.get(self.public_base_url + '/auction/' + product_id)
        else:
            self.timestamp = time.mktime(datetime.datetime.strptime(since,
                                                                    "%d/%m/%Y").timetuple())
            r = requests.get(self.public_base_url + '/auction/{}?since={}'.format(
                product_id, int(self.timestamp)))
        return r.json()

        @typeassert(product_id=str)
        def get_ticker_v2(self, product_id):
            """
            This endpoint retrieves information about recent trading
            activity for the symbol.

            Args:
                product_id(str): Can be any value in self.symbols()

            Returns:
                    dict: the Open, High, and Low price from 24 hours ago,
                    the Close price (most recent trade),
                    Hourly prices descending for past 24 hours,
                    and the current bid and ask

                    example: {
                              "symbol": "BTCUSD",
                              "open": "9121.76",
                              "high": "9440.66",
                              "low": "9106.51",
                              "close": "9347.66",
                              "changes": [
                                "9365.1",
                                "9386.16",
                                "9373.41",
                                "9322.56",
                                "9268.89",
                                "9265.38",
                                "9245",
                                "9231.43",
                                "9235.88",
                                "9265.8",
                                "9295.18",
                                "9295.47",
                                "9310.82",
                                "9335.38",
                                "9344.03",
                                "9261.09",
                                "9265.18",
                                "9282.65",
                                "9260.01",
                                "9225",
                                "9159.5",
                                "9150.81",
                                "9118.6",
                                "9148.01"
                              ],
                              "bid": "9345.70",
                              "ask": "9347.67"
                            }
            """
            r = requests.get('https://api.gemini.com/v2'
                             + '/ticker/' + product_id)
            return r.json()
