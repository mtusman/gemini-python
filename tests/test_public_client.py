import sys
sys.path.insert(0, '..')
from gemini import PublicClient


def client():
    return PublicClient(sandbox=True)


class TestPublicClient:
    def test_get_ticker(self):
        r = client()
        ticker = r.get_ticker("BTCUSD")
        assert type(ticker) is dict
        assert "bid" in ticker
        assert "ask" in ticker
        assert "volume" in ticker
        assert "last" in ticker

    def test_get_current_order_book(self):
        r = client()
        order_book = r.get_current_order_book("BTCUSD")
        assert type(order_book) is dict
        assert "bid" or "ask" in order_book

    def test_get_trade_history(self):
        r = client()
        trade_history = r.get_trade_history("BTCUSD")
        assert type(trade_history) is list
        assert "timestamp" in trade_history[0]
        assert "timestampms" in trade_history[0]
        assert "tid" in trade_history[0]
        assert "price" in trade_history[0]
        assert "amount" in trade_history[0]
        assert "exchange" in trade_history[0]
        assert "type" in trade_history[0]

    def test_get_auction_history(self):
        r = client()
        auction_history = r.get_auction_history("BTCUSD")
        assert auction_history is list or dict

    def test_symbols(self):
        r = client()
        symbols = r.symbols()
        assert type(symbols) is list

    def test_symbol_details(self):
        r = client()
        symbol_details = r.symbol_details("BTCUSD")
        assert type(symbol_details) is dict
        assert "symbol" in symbol_details
        assert "base_currency" in symbol_details
        assert "quote_currency" in symbol_details
        assert "tick_size" in symbol_details
        assert "quote_increment" in symbol_details
        assert "min_order_size" in symbol_details
        assert "status" in symbol_details
        assert "wrap_enabled" in symbol_details
