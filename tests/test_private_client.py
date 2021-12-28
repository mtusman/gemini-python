from .keys import public_key, private_key
import sys
sys.path.insert(0, '..')
from gemini import PrivateClient


def client():
    return PrivateClient(public_key, private_key, sandbox=True)


class TestPrivateClient:
    def test_new_order(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        assert type(new_order) is dict
        assert "order_id" in new_order
        assert "id" in new_order
        assert "symbol" in new_order
        assert "exchange" in new_order
        assert "avg_execution_price" in new_order
        assert "side" in new_order
        assert "type" in new_order
        assert "timestamp" in new_order
        assert "timestampms" in new_order
        assert "is_live" in new_order
        assert "is_cancelled" in new_order
        assert "is_hidden" in new_order
        assert "was_forced" in new_order
        assert "executed_amount" in new_order
        assert "remaining_amount" in new_order
        assert "options" in new_order
        assert "price" in new_order
        assert "original_amount" in new_order

    def test_cancel_order(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        cancel_order = r.cancel_order(new_order["order_id"])
        assert type(cancel_order) is dict
        assert "order_id" in cancel_order
        assert "id" in cancel_order
        assert "symbol" in cancel_order
        assert "exchange" in cancel_order
        assert "avg_execution_price" in cancel_order
        assert "side" in cancel_order
        assert "type" in cancel_order
        assert "timestamp" in cancel_order
        assert "timestampms" in cancel_order
        assert "is_live" in cancel_order
        assert "is_cancelled" in cancel_order
        assert "is_hidden" in cancel_order
        assert "was_forced" in cancel_order
        assert "executed_amount" in cancel_order
        assert "remaining_amount" in cancel_order
        assert "options" in cancel_order
        assert "price" in cancel_order
        assert "original_amount" in cancel_order

    def test_cancel_session_orders(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        cancel_session_orders = r.cancel_session_orders()
        assert type(cancel_session_orders) is dict
        assert "result" in cancel_session_orders
        assert "details" in cancel_session_orders

    def test_cancel_orders(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        cancel_all_orders = r.cancel_all_orders()
        assert type(cancel_all_orders) is dict
        assert "result" in cancel_all_orders
        assert "details" in cancel_all_orders

    def test_wrap_order(self):
        r = client()
        wrap_order = r.wrap_order("GUSDUSD", "10", "buy")
        assert type(wrap_order) is dict
        # Endpoint not supported on sandbox
        assert "error" in wrap_order #{'error': 'Encountered an error attempting to place a wrap/unwrap trade.'}
        # assert "orderId" in wrap_order
        # assert "pair" in wrap_order
        # assert "price" in wrap_order
        # assert "priceCurrency" in wrap_order
        # assert "side" in wrap_order
        # assert "quantity" in wrap_order 
        # assert "quantityCurrency" in wrap_order
        # assert "totalSpend" in wrap_order
        # assert "totalSpendCurrency" in wrap_order 
        # assert "fee" in wrap_order
        # assert "feeCurrency" in wrap_order
        # assert "depositFee" in wrap_order
        # assert "depositFeeCurrency" in wrap_order

    def test_status_of_orders(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        status_of_order = r.status_of_order(new_order["order_id"])
        assert type(status_of_order) is dict
        assert "order_id" in status_of_order
        assert "id" in status_of_order
        assert "symbol" in status_of_order
        assert "exchange" in status_of_order
        assert "avg_execution_price" in status_of_order
        assert "side" in status_of_order
        assert "type" in status_of_order
        assert "timestamp" in status_of_order
        assert "timestampms" in status_of_order
        assert "is_live" in status_of_order
        assert "is_cancelled" in status_of_order
        assert "is_hidden" in status_of_order
        assert "was_forced" in status_of_order
        assert "executed_amount" in status_of_order
        assert "remaining_amount" in status_of_order
        assert "options" in status_of_order
        assert "price" in status_of_order
        assert "original_amount" in status_of_order

    def test_active_orders(self):
        r = client()
        new_order = r.new_order("BTCUSD", "0.02", "6400.28", "buy", ["maker-or-cancel"])
        active_orders = r.active_orders()
        assert type(active_orders) is list

    def test_get_past_trades(self):
        r = client()
        get_past_trades = r.get_past_trades("BTCUSD")
        assert type(get_past_trades) is list

    def test_get_trade_volume(self):
        r = client()
        get_trade_volume = r.get_trade_volume()
        assert type(get_trade_volume) is list

    def test_get_balance(self):
        r = client()
        get_past_trades = r.get_past_trades("BTCUSD")
        assert type(get_past_trades) is list

    def test_get_balance(self):
        r = client()
        get_balance = r.get_balance()
        assert type(get_balance) is list

    def test_create_deposit_address(self):
        r = client()
        create_deposit_address = r.create_deposit_address("ETH", label="testing")
        assert type(create_deposit_address) is dict

    def test_withdraw_to_address(self):
        r = PrivateClient("PUBLIC_KEY", "PRIVATE_CLIENT")
        withdraw_to_address = r.withdraw_to_address("ETH", "200", "0x0287b1B0032Dc42c16640F71BA06F1A87C3a7101")
        assert type(withdraw_to_address) is dict

    def test_revive_heartbeat(self):
        r = client()
        revive_hearbeat = r.revive_hearbeat()
        assert type(revive_hearbeat) is dict
