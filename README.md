# gemini-python
A python client for the Gemini API and Websocket

## Getting Started
### Installation
```python
pip install gemini_python
```
### PublicClient
This endpoint doesn't require an api-key and can
be used without having a Gemini account. This README
will document some of the methods and features of the class.
```python
import gemini
r = gemini.PublicClient()
# Alternatively, for a sandbox environment, set sandbox=True
r = gemini.PublicClient(sandbox=True)
```
#### PublicClient Methods
- [symbols](https://docs.gemini.com/rest-api/#symbols)
```python
r.symbols()
```
- [get_ticker](https://docs.gemini.com/rest-api/#ticker)
```python
r.get_ticker("BTCUSD")
```
- [get_current_order_book](https://docs.gemini.com/rest-api/#current-order-book)
```python
r.get_current_order_book("BTCUSD")
```
- [get_trade_history](https://docs.gemini.com/rest-api/#trade-history)
```python
# Will get the latest 500 trades
r.get_trade_history("BTCUSD")
# Alternatively, it can be specified for a specific date
r.get_trade_history("BTCUSD", since="17/06/2017")
```
- [get_auction_history](https://docs.gemini.com/rest-api/#current-auction)
```python
# Will get the latest 500 auctions
r.get_auction_history("BTCUSD")
# Alternatively, it can be specified for a specific date
r.get_auction_history("BTCUSD", since="17/06/2017")
```

### PrivateClient
This endpoint requires both a public and private key to access
the API. Hence, one must have an account with Gemini and register an
application. So far, if the 'heartbeat' option is enabled for the API,
the user must manually revive the heartbeat. Further options will be added
in the future in order to avoid doing this manually.

The payload of the requests
will be a JSON object. Rather than being sent as the body of the POST request,
Gemini requires it to be base-64 encoded and stored as a header in the request.
Adding a 'nonce' is optional for the API but is highly recommended. That's why
the class will always send each request with a unique 'nonce'. An important
point to note is that every argument for the methods of PrivateClient must be
strings with the exception of 'options'.

```python
import gemini
r = gemini.PrivateClient("EXAMPLE_PUBLIC_KEY", "EXAMPLE_PRIVATE_KEY")
# Alternatively, for a sandbox environment, set sandbox=True
r = gemini.PrivateClient("EXAMPLE_PUBLIC_KEY", "EXAMPLE_PRIVATE_KEY", sandbox=True)
```

#### PrivateClient Methods
- [new_order](https://docs.gemini.com/rest-api/#new-order)
```python
r.new_order("BTCUSD", "200", "6000", "buy")
```
- [cancel_order](https://docs.gemini.com/rest-api/#cancel-order)
```python
r.cancel_order("866403510")
```
- [cancel_session_orders](https://docs.gemini.com/rest-api/#cancel-all-session-orders)
```python
r.cancel_session_orders()
```
- [cancel_all_orders](https://docs.gemini.com/rest-api/#cancel-all-active-orders)
```python
r.cancel_all_orders()
```
- [status_of_order](https://docs.gemini.com/rest-api/#order-status)
```python
r.status_of_order("866403510")
```
- [active_orders](https://docs.gemini.com/rest-api/#get-active-orders)
```python
r.active_orders()
```
- [get_past_trades](https://docs.gemini.com/rest-api/#get-past-trades)
```python
# Will get the last 500 past trades
r.get_past_trades("BTCUSD")
# Alternatively, you can set the limit_trades number to your liking
r.get_past_trades("BTCUSD", limit_trades="200")
```
- [get_trade_volume](https://docs.gemini.com/rest-api/#get-trade-volume)
```python
r.get_trade_volume()
```
- [get_balance](https://docs.gemini.com/rest-api/#get-available-balances)
```python
r.get_balance()
```
- [create_deposit_address](https://docs.gemini.com/rest-api/#new-deposit-address)
```python
# This will create a new currency address
r.create_deposit_address("BTCUSD")
# Alternatively, you can specify the label
r.create_deposit_address("BTCUSD", label="Main Bitcoin Address")
```
- [withdraw_to_address](https://docs.gemini.com/rest-api/#withdraw-crypto-funds-to-whitelisted-address)
```python
r.withdraw_to_address("ETH", "0x0287b1B0032Dc42c16640F71BA06F1A87C3a7101", "20")
```
- [revive_hearbeat](https://docs.gemini.com/rest-api/#ticker)
```python
r.revive_hearbeat()
```
### Websocket Client 
If you'd prefer to recieve live updates you can either choose to subsribe to the public market data websocket or the private order events websocket. For more information about the difference between the two websockets visit the official [Gemini documentation](https://docs.gemini.com/websocket-api).

### MarketData Websocket 
Market data is a public API that streams all the market data on a given symbol.
```python
import gemini
r = gemini.MarketDataWS('btcusd')
# Alternatively, for a sandbox environment, set sandbox=True
r = gemini.MarketDataWS('btcusd', sandbox=True)
```
#### MarketData Websocket Methods 
- get list of recorded trades
```python
r.trades
```
- get recorded bids
```python
r.bids
```
- get recorded asks
```python
r.asks
```
- get market book
```python
r.get_market_book()
```
- remove a recorded price from bids or asks
```python
# To remove a price from bids
r.remove_from_bids('10000')
# To remove a price from asks
r.remove_from_asks('10000')
```
- search for a particular price recorded
```python
r.search_price('10000')
```
- export recorded trades to csv
```python
r.export_to_csv(r'/c/Users/user/Documents')
```
- export recorded trades to xml
```python
r.export_to_xml(r'/c/Users/user/Documents')
```
### OrderEvents Websocket
Order events is a private API that gives you information about your orders in real time.When you connect, you get a book of your active orders. Then in real time you'll get information about order events like:

- when your orders are accepted by the exchange
- when your orders first appear on the book
- fills
- cancels
- and more.


Support for subscription filters is currently under development

```python
import gemini
r = gemini.OrderEventsWS("EXAMPLE_PUBLIC_KEY", "EXAMPLE_PRIVATE_KEY")
# Alternatively, for a sandbox environment, set sandbox=True
r = gemini.OrderEventsWS("EXAMPLE_PUBLIC_KEY", "EXAMPLE_PRIVATE_KEY", sandbox=True)
```

#### OrderEvents Websocket Methods 
- get order types
```python
"""All trades are categorised in terms of either subscription_ack', 'heartbeat', 
'initial', 'accepted','rejected', 'booked', 'fill', 'cancelled', 
'cancel_rejected' or 'closed'. The following will print these types"""
r.get_order_types
```
- get order book
```python
# Will return all recorded orders
r.get_order_book
```
- remove a recorded price from the order book
```python
# Arguments are: type and order_id
r.remove_order('accepted', '12321123')
```
- export recorded trades to csv
```python
# Arguments are: directory and type
# The following will export all 'accepted' orders to a csv format
r.export_to_csv(r'/c/Users/user/Documents', 'accepted')
```
- export recorded trades to xml
```python
# Arguments are: directory and type. 
# The following will export all 'accepted' orders to a xml format
r.export_to_xml(r'/c/Users/user/Documents', 'accepted')
```  

# Under Development
- Add filter options to order events websocket
- Improve options to add and remove orders from market data websocket
- Add options to choose whether a particular class is cached or not
- Export recorded data from market data or order events websocket into a matplotlib graph
- Export recorded data from market data or order events websocket into a sqlite, postgresl or sql database
- Add test for the cached metaclass

# Change Log
*0.2.0*
- Created BaseWebsocket class 
- Created OrderEventsWS class to interact with the order events websocket
- Created MarketDataWS class to interact with the market data websocket 
- Added greater support for heartbeat API's
- Improved the Cached metaclass
- Added support for sandbox urls 

*0.0.1*
- Original release