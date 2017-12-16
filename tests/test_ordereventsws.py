from .keys import public_key, private_key
import sys
import os
import time
sys.path.insert(0, '..')
from gemini import OrderEventsWS


def client():
    return OrderEventsWS(public_key, private_key, sandbox=True)


class TestOrderEventsWS:
    def test_filter(self):
        r = OrderEventsWS(public_key, private_key, sandbox=False)
        assert r.base_url == 'wss://api.gemini.com/v1/order/events'
        # Testing that symbol filter is working
        r = OrderEventsWS(public_key, private_key, symbolFilter=['btcusd', 'ethusd'])
        assert r.base_url == ('wss://api.gemini.com/v1/order/events?' +
                              'symbolFilter=btcusd&symbolFilter=ethusd')
        # Testing that event type filter is working
        r = OrderEventsWS(public_key, private_key, eventTypeFilter=['accepted'])
        assert r.base_url == ('wss://api.gemini.com/v1/order/events?' +
                              'eventTypeFilter=accepted')
        # Testing that api session filter is working
        r = OrderEventsWS(public_key, private_key, apiSessionFilter=['lVTsC8CfoxkbkHVBKjEu'])
        assert r.base_url == ('wss://api.gemini.com/v1/order/events?' +
                              'apiSessionFilter=lVTsC8CfoxkbkHVBKjEu')
        # Testing all filters work correctly when used together
        r = OrderEventsWS(public_key, private_key, symbolFilter=['btcusd', 'ethusd'],
                          eventTypeFilter=['accepted'],
                          apiSessionFilter=['lVTsC8CfoxkbkHVBKjEu'])
        assert r.base_url == ('wss://api.gemini.com/v1/order/events?' +
                              'symbolFilter=btcusd&symbolFilter=ethusd&' +
                              'eventTypeFilter=accepted&' +
                              'apiSessionFilter=lVTsC8CfoxkbkHVBKjEu')

    def test_reset_order_book(self):
        r = client()
        r._reset_order_book()
        for key in r.order_book.keys():
            assert len(r.order_book[key]) == 0

    def test_api_query(self):
        r = client()
        r.start()
        time.sleep(5)
        assert len(r.order_book['subscription_ack']) != 0
        r.close()

    def test_on_message(self):
        r = client()
        for key in r.order_book.keys():
            assert len(r.order_book[key]) == 0
        r.on_message({'accountId': 2117,
                      'apiSessionFilter': [],
                      'eventTypeFilter': [],
                      'subscriptionId': 'ws-order-events-2117-b01s1aqlv776oceke7t0',
                      'symbolFilter': [],
                      'type': 'subscription_ack'})
        for key in r.order_book.keys():
            if key == "subscription_ack":
                assert len(r.order_book[key]) == 1
            else:
                assert len(r.order_book[key]) == 0
        r.on_message({'sequence': 0,
                      'socket_sequence': 0,
                      'timestampms': 1512080326919,
                      'trace_id': 'b01s1aqlv776oceke7t0',
                      'type': 'heartbeat'})
        for key in r.order_book.keys():
            if key == "subscription_ack" or key == "heartbeat":
                assert len(r.order_book[key]) == 1
            else:
                assert len(r.order_book[key]) == 0
        for key in r.order_book.keys():
            if key != "subscription_ack" and key != "heartbeat":
                r.on_message([{'api_session': 'lVTsC8CfoxkbkHVBKjEu',
                               'behavior': 'immediate-or-cancel',
                               'event_id': '86560107',
                               'is_cancelled': False,
                               'is_hidden': False,
                               'is_live': True,
                               'order_id': '86560106',
                               'order_type': 'exchange limit',
                               'original_amount': '0.1',
                               'price': '10000.00',
                               'side': 'buy',
                               'socket_sequence': 38,
                               'symbol': 'btcusd',
                               'timestamp': '1512080804',
                               'timestampms': 1512080804958,
                               'type': '{}'.format(key)}])
        for key in r.order_book.keys():
            assert len(r.order_book[key]) == 1

    def test_remove_order(self):
        r = client()
        r.on_message([{'api_session': 'lVTsC8CfoxkbkHVBKjEu',
                       'behavior': 'immediate-or-cancel',
                       'event_id': '86560107',
                       'is_cancelled': False,
                       'is_hidden': False,
                       'is_live': True,
                       'order_id': '86560106',
                       'order_type': 'exchange limit',
                       'original_amount': '0.1',
                       'price': '10000.00',
                       'side': 'buy',
                       'socket_sequence': 38,
                       'symbol': 'btcusd',
                       'timestamp': '1512080804',
                       'timestampms': 1512080804958,
                       'type': 'accepted'}])
        assert len(r.order_book['accepted']) == 1
        r.remove_order('accepted', '86560106')
        assert len(r.order_book['accepted']) == 0

    def test_export_to_csv(self):
        r = client()
        r.on_message({'sequence': 0,
                      'socket_sequence': 0,
                      'timestampms': 1512080326919,
                      'trace_id': 'b01s1aqlv776oceke7t0',
                      'type': 'heartbeat'})
        r.export_to_csv(r'{}'.format(os.getcwd()), 'heartbeat')
        assert "gemini_order_events.csv" in os.listdir(r'{}'.format(os.getcwd()))
        os.remove("gemini_order_events.csv")

    def test_export_to_xml(self):
        r = client()
        r.on_message({'sequence': 0,
                      'socket_sequence': 0,
                      'timestampms': 1512080326919,
                      'trace_id': 'b01s1aqlv776oceke7t0',
                      'type': 'heartbeat'})
        r.export_to_xml(r'{}'.format(os.getcwd()), 'heartbeat')
        assert "gemini_order_events.xml" in os.listdir(r'{}'.format(os.getcwd()))
        os.remove("gemini_order_events.xml")
