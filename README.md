# gemini-python-wrapper
A python client for the gemini API

## Getting Started
### PublicClient
This endpoint doesn't require an api-key and can
be used without having a gemini account. This README
will document some of the methods and features of the class.
```python
import gemini
r = gemini.PublicClient()
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
# Note: 'since' is a keyword argument!
```
- [get_auction_history](https://docs.gemini.com/rest-api/#current-auction)
```python
# Will get the latest 500 auctions
r.get_auction_history("BTCUSD")
# Alternatively, it can be specified for a specific date
r.get_auction_history("BTCUSD", since="17/06/2017")
# Note: 'since' is again a keyword argument!
```

### PrivateClient
This endpoint requires both a public and private key to access
the API. Hence, one must have an account with gemini and register an
application. So far, if the 'heartbeat' option is enabled for the API,
the user must manually revive the heartbeat. Further options will be added
in the future in order to avoid doing this manually.

The payload of the requests
will be a JSON object. Rather than being sent as the body of the POST request,
gemini requires it to be base-64 encoded and stored as a header in the request.
Adding a 'nonce' is optional for the API but is highly recommended. That's why
the class will always send each request with a unique 'nonce'. An important
point to note is that every argument for the methods of PrivateClient must be
strings with the exception of 'options'.

```python
import gemini
r = gemini.PrivateClient("EXAMPLE_PUBLIC_KEY", "EXAMPLE_PRIVATE_KEY")
```

#### PrivateClient Methods
- [new_order](https://docs.gemini.com/rest-api/#new-order)
```python
r.new_order("BTCUSD", "200", "6000", "buy", ["immediate-or-cancel"])
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

# Under Development
- Base Websocket Class
- [Support for Market Data Websocket](https://docs.gemini.com/websocket-api/#market-data)
- [Support for Order Events Websocket](https://docs.gemini.com/websocket-api/#order-events)
- Greater support for hearbeat API's
