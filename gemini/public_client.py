# public_client.py
# Mohammad Usman
#
# A python wrapper for Gemini's public API

from cached import Cached
import requests
import time
import datetime


class PublicClient(metaclass=Cached):
    def __init__(self):
        self.public_base_url = 'https://api.gemini.com/v1'

    def get_ticker(self, product_id):
        ''' This endpoint retrieves information about recent trading
        activity for the symbol

        Returns:
                dict: the latest bid, ask, last price qouted and the volume
                example: {
                  "bid": "4269.50",
                  "ask": "4269.51",
                  "volume": {
                    "BTC": "5586.1638562221",
                    "USD": "24176720.342631938501",
                    "timestamp": 1507060200000
                  },
                  "last": "4269.50"
                }
        '''
        r = requests.get(self.public_base_url + '/pubticker/' + product_id)
        return r.json()

    def get_current_order_book(self, product_id):
        ''' This endpoint retreives information about the recents orders

        Returns:
            dict: This will return the current order book, as two arrays,
            one of bids, and one of asks
            example:{
              "bids": [ /* bids look like asks */ ],
              "asks": [
                {
                  "price": "822.12",  // Note these are sent as strings
                  "amount": "12.1"  // Ditto
                },
                ...
              ]
            }
        '''
        r = requests.get(self.public_base_url + '/book/' + product_id)
        return r.json()

    def get_trade_history(self, product_id, *, since=None):
        ''' This endpoint will return the trades that have executed since the
        specified timestamp. Timestamps are either seconds or milliseconds
        since the epoch (1970-01-01).

        Returns:
            format: 'since' must be in DD/MM/YYYY format
            list: Will return at most 500 records
            example:[
              {
                "timestamp": 1420088400,
                "timestampms": 1420088400122,
                "tid": 155814,
                "price": "822.12",
                "amount": "12.10",
                "exchange": "gemini",
                "type": "buy"
              },
              ...
            ]
        '''
        if since is None:
            r = requests.get(self.public_base_url + '/trades/' + product_id)
        else:
            self.timestamp = time.mktime(datetime.datetime.strptime(since,
                                                                    "%d/%m/%Y").timetuple())
            r = requests.get(self.public_base_url + '/trades/{}?since={}'.format(
                product_id, int(self.timestamp)))
        return r.json()

    def get_auction_history(self, product_id, *, since=None):
        ''' This will return the auction events, optionally including 
        publications of indicative prices, since the specific timestamp.

        Returns:
            format: 'since' must be in DD/MM/YYYY format
            list: Will return at most 500 records
            example:[
                {
                    "auction_id": 3,
                    "auction_price": "628.775",
                    "auction_quantity": "66.32225622",
                    "eid": 4066,
                    "highest_bid_price": "628.82",
                    "lowest_ask_price": "629.48",
                    "auction_result": "success",
                    "timestamp": 1471902531,
                    "timestampms": 1471902531225,
                    "event_type": "auction"
                },
                ...
            ]
        '''
        if since is None:
            r = requests.get(self.public_base_url + '/auction/' + product_id)
        else:
            self.timestamp = time.mktime(datetime.datetime.strptime(since,
                                                                    "%d/%m/%Y").timetuple())
            r = requests.get(self.public_base_url + '/auction/{}?since={}'.format(
                product_id, int(self.timestamp)))
        return r.json()

    @classmethod
    def symbols(self):
        ''' This endpoint retrieves all available symbols for trading

        Returns:
            list: Will output an array of supported symbols
            example: [ "btcusd", "ethusd", "ethbtc" ]
        '''
        r = requests.get(self.public_base_url + '/symbols')
        return r.json()
