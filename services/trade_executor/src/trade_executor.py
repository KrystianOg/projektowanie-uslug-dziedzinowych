import os 
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import TimeInForce
from models import Signal

import logging
logger = logging.getLogger(__name__)

ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', '')
ALPACA_SECRET =os.getenv('ALPACA_SECRET', '')

trading_client = TradingClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET, paper=True)

class TradeExecutor:
    history: list[MarketOrderRequest] = []

    def order(self, signal: Signal):
        quantity = self._calculate_quantity(signal)
        market_order_data = MarketOrderRequest(
            symbol=signal.symbol,
            qty=quantity,
            side=signal.action,
            time_in_force=TimeInForce.DAY
        )
        trading_client.submit_order(order_data=market_order_data)
        self.history.append(market_order_data)
        logger.info(f"Made a trade {signal.action} {quantity} {signal.symbol}")


    def close_all_positions(self):
        """
        Closes all open positions and cancels all open orders. 
        Only use in some critical situations!
        """
        trading_client.close_all_positions(cancel_orders=True)

    def _calculate_quantity(self, signal: Signal) -> float:
        return 100.0 
