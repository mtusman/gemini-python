import sys
import os
sys.path.insert(0, '..')
from gemini import MarketDataWS


def client():
    return MarketDataWS('btcusd', sandbox=True)


class TestMarketDataWS:
    def test_on_message(self):
        r = client()
        r.on_message({'eventId': 2364280145,
                      'events': [{'delta': '-19.52358571',
                                  'price': '9594.37',
                                  'reason': 'cancel',
                                  'remaining': '0',
                                  'side': 'bid',
                                  'type': 'change'}],
                      'socket_sequence': 0,
                      'timestamp': 1512076260,
                      'timestampms': 1512076260185,
                      'type': 'update'})
        assert len(r.asks) == 0
        assert len(r.bids) == 0
        assert len(r.trades) == 0
        r.on_message({'eventId': 2364280145,
                      'events': [{'delta': '-19.52358571',
                                  'price': '9594.37',
                                  'reason': 'cancel',
                                  'remaining': '0',
                                  'side': 'bid',
                                  'type': 'change'}],
                      'socket_sequence': 1,
                      'timestamp': 1512076260,
                      'timestampms': 1512076260185,
                      'type': 'update'})
        assert len(r.asks) == 0
        assert len(r.bids) == 0
        assert len(r.trades) == 0
        r.on_message({'eventId': 2364281810,
                      'events': [{'amount': '0.3865',
                                  'makerSide': 'ask',
                                  'price': '9610.40',
                                  'tid': 2364281810,
                                  'type': 'trade'},
                                 {'delta': '-0.3865',
                                  'price': '9610.40',
                                  'reason': 'trade',
                                  'remaining': '1.7439',
                                  'side': 'ask',
                                  'type': 'change'}],
                      'socket_sequence': 884,
                      'timestamp': 1512076268,
                      'timestampms': 1512076268486,
                      'type': 'update'})
        assert len(r.asks) == 1
        assert len(r.bids) == 0
        assert len(r.trades) == 1
        r.on_message({'eventId': 2364281810,
                      'events': [{'amount': '0.3865',
                                  'makerSide': 'bid',
                                  'price': '9610.40',
                                  'tid': 2364281810,
                                  'type': 'trade'},
                                 {'delta': '-0.3865',
                                  'price': '9610.40',
                                  'reason': 'trade',
                                  'remaining': '1.7439',
                                  'side': 'ask',
                                  'type': 'change'}],
                      'socket_sequence': 884,
                      'timestamp': 1512076268,
                      'timestampms': 1512076268486,
                      'type': 'update'})
        assert len(r.asks) == 1
        assert len(r.bids) == 1
        assert len(r.trades) == 2

    def test_get_market_book(self):
        r = client()
        assert type(r.get_market_book()) is dict

    def test_reset_market_book(self):
        r = client()
        r.reset_market_book()
        assert len(r.asks) == 0
        assert len(r.bids) == 0

    def test_search_price(self):
        r = client()
        r.add('bid', {'eventId': 2364281810,
                      'events': [{'amount': '0.3865',
                                  'makerSide': 'bid',
                                  'price': '10000',
                                  'tid': 2364281810,
                                  'type': 'trade'},
                                 {'delta': '-0.3865',
                                  'price': '10000',
                                  'reason': 'trade',
                                  'remaining': '1.7439',
                                  'side': 'bid',
                                  'type': 'change'}],
                      'socket_sequence': 885,
                      'timestamp': 1512076268,
                      'timestampms': 1512076268486,
                      'type': 'update'})
        result = r.search_price('10000')
        assert type(result) is dict
        assert "price" in result
        assert len(result["price"]) != 0

    def test_remove_from_bids(self):
        r = client()
        r.add('bid', {'eventId': 2364281810,
                      'events': [{'amount': '0.3865',
                                  'makerSide': 'bid',
                                  'price': '11000',
                                  'tid': 2364281810,
                                  'type': 'trade'},
                                 {'delta': '-0.3865',
                                  'price': '11000',
                                  'reason': 'trade',
                                  'remaining': '1.7439',
                                  'side': 'bid',
                                  'type': 'change'}],
                      'socket_sequence': 886,
                      'timestamp': 1512076268,
                      'timestampms': 1512076268486,
                      'type': 'update'})
        search = r.search_price('11000')
        assert len(search['price']) == 1
        r.remove_from_bids('11000')
        search = r.search_price('11000')
        assert len(search['price']) == 0

    def test_remove_from_asks(self):
        r = client()
        r.add('ask', {'eventId': 2364281810,
                      'events': [{'amount': '0.3865',
                                  'makerSide': 'ask',
                                  'price': '12000',
                                  'tid': 2364281810,
                                  'type': 'trade'},
                                 {'delta': '-0.3865',
                                  'price': '12000',
                                  'reason': 'trade',
                                  'remaining': '1.7439',
                                  'side': 'ask',
                                  'type': 'change'}],
                      'socket_sequence': 886,
                      'timestamp': 1512076268,
                      'timestampms': 1512076268486,
                      'type': 'update'})
        search = r.search_price('12000')
        assert len(search['price']) == 1
        r.remove_from_asks('12000')
        search = r.search_price('12000')
        assert len(search['price']) == 0

    def test_export_to_csv(self):
        r = client()
        r.export_to_csv(r'{}'.format(os.getcwd()))
        assert "gemini_market_data.csv" in os.listdir(r'{}'.format(os.getcwd()))
        os.remove("gemini_market_data.csv")

    def test_export_to_xml(self):
        r = client()
        r.export_to_xml(r'{}'.format(os.getcwd()))
        assert "gemini_market_data.xml" in os.listdir(r'{}'.format(os.getcwd()))
        os.remove("gemini_market_data.xml")
