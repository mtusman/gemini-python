# basewebsocket.py
# Mohammad Usman
#
# This class is to be used as the parent for the MarketWebsocket and
# OrderWebsocket
from .cached import Cached
from .debugly import typeassert
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
import json


class BaseWebSocket(metaclass=Cached):
    @typeassert(base_url=str)
    def __init__(self, base_url):
        self.base_url = base_url
        self.ws = None
        self.messages = 0

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()
        self.stop = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.thread.start()

    def _connect(self):
        self.ws = create_connection(self.base_url)

    def _listen(self):
        while not self.stop:
            try:
                data = self.ws.recv()
            except ValueError as e:
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(json.loads(data))

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
                self.on_close()
        except WebSocketConnectionClosedException as e:
            self.on_error(e)

    def close(self):
        self.stop = True
        self.thread.join()

    def on_open(self):
        print('--Subscribed--\n')

    def on_message(self, msg):
        print(msg)
        self.messages += 1

    def on_error(self, e):
        print(e)

    def on_close(self):
        print('\n--Ended Connection--')
