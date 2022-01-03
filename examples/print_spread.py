#!/usr/bin/env python3

import time

from gemini.order_book import GeminiOrderBook

book = GeminiOrderBook('ETHUSD')
book.start()
time.sleep(5) # needs a bit of time to populate the order book
while(True):
    print("Spread: %f" % (book.get_ask() - book.get_bid()))
    time.sleep(1)
