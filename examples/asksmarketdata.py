# askmarketdata.py
# Mohammad Usman
#
# A simple example showing how the BaseWebSocket class can be modified.
# AsksWebSocket will print the latest 100 ask orders and then close the
# connection

import sys
sys.path.insert(0, '..')
from gemini.basewebsocket import BaseWebSocket
from collections import deque


class AsksWebSocket(BaseWebSocket):
    def __init__(self, base_url):
        super().__init__(base_url)
        self._asks = deque(maxlen=100)

    def on_open(self):
        print('--Subscribed to asks orders!--\n')

    def on_message(self, msg):
        try:
            event = msg['events'][0]
            if event['type'] == 'trade' and event['makerSide'] == 'ask':
                print(msg)
                self._asks.append(msg['events'])
                self.messages += 1
        except KeyError as e:
            pass


if __name__ == '__main__':
    wsClient = AsksWebSocket('wss://api.gemini.com/v1/marketdata/btcusd')
    wsClient.start()
    while True:
        if wsClient.messages >= 100:
            wsClient.close()
            break
