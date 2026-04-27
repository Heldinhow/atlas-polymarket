"""Base execution class."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Trade:
    """Represents a trade."""
    market_id: str
    side: str  # BUY or SELL
    amount: float
    price: float
    timestamp: datetime
    status: str = "PENDING"


class BaseExecutor(ABC):
    """Abstract base for trade executors."""

    @abstractmethod
    def place_trade(
        self,
        market_id: str,
        side: str,
        amount: float,
        price: float,
    ) -> dict[str, Any]:
        """Place a trade."""
        pass

    @abstractmethod
    def get_balance(self) -> float:
        """Get current balance."""
        pass

    @abstractmethod
    def get_positions(self) -> list[dict[str, Any]]:
        """Get current positions."""
        pass
