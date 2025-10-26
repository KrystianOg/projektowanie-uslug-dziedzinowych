from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime
from alpaca.trading.enums import OrderSide

import logging
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Signal:
    """Validated trading signal
    
    Attributes:
        symbol: Trading symbol (e.g., 'BTC/USD')
        action: Buy or sell action
        confidence: Confidence level (0.0 to 1.0)
        timestamp: Signal generation time
    """
    symbol: str
    action: OrderSide
    confidence: float
    timestamp: datetime 

    def __post_init__(self):
        """Validate field constraints"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")

        if not self.symbol or not self.symbol.strip():
            raise ValueError("Symbol cannot be empty")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Optional["Signal"]:
        try:
            symbol = data.get('symbol')
            if not isinstance(symbol, str):
                logger.warning(f"Invalid symbol type: {type(symbol)}")
                return None

            action_str = data.get('action')
            if action_str not in ('buy', 'sell'):
                logger.warning(f"Invalid action value: {action_str}")
                return None

            confidence = data.get('confidence')
            if not isinstance(confidence, (float, int)):
                logger.warning(f"INvalid confidence type: {type(confidence)}")
                return None

            timestamp_raw = data.get('timestamp')
            if isinstance(timestamp_raw, str):
                timestamp = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
            elif isinstance(timestamp_raw, datetime):
                timestamp = timestamp_raw
            else:
                logger.warning(f"Invalid timestamp type: {type(timestamp_raw)}")
                return None

            return cls(
                symbol=symbol,
                action=OrderSide(action_str),
                confidence=float(confidence),
                timestamp=timestamp
            )
            
        except (ValueError, KeyError) as e:
            logger.error(f"Signal validation failed: {e}", exc_info=True)
            return None
