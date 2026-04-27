"""Paper trading executor - simulates trades without real money."""
from typing import Any
from src.execution.base import BaseExecutor, Trade


class PaperTrader(BaseExecutor):
    """Paper trading executor for testing strategies."""

    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.trades: list[Trade] = []
        self.positions: dict[str, dict[str, Any]] = {}

    def place_trade(
        self,
        market_id: str,
        side: str,
        amount: float,
        price: float,
    ) -> dict[str, Any]:
        """Place a simulated trade."""
        cost = amount * price

        if side == "BUY":
            if cost > self.balance:
                return {"status": "REJECTED", "reason": "Insufficient balance"}
            self.balance -= cost

            if market_id in self.positions:
                pos = self.positions[market_id]
                total_amount = pos["amount"] + amount
                avg_price = (pos["cost"] + cost) / total_amount
                pos["amount"] = total_amount
                pos["cost"] = avg_price * total_amount
            else:
                self.positions[market_id] = {
                    "amount": amount,
                    "cost": cost,
                    "avg_price": price,
                }
        else:  # SELL
            if market_id not in self.positions:
                return {"status": "REJECTED", "reason": "No position to sell"}

            pos = self.positions[market_id]
            if pos["amount"] < amount:
                return {"status": "REJECTED", "reason": "Insufficient position"}

            proceeds = amount * price
            self.balance += proceeds
            pos["amount"] -= amount
            if pos["amount"] == 0:
                del self.positions[market_id]

        trade = Trade(
            market_id=market_id,
            side=side,
            amount=amount,
            price=price,
            timestamp=__import__("datetime").datetime.now(),
            status="FILLED",
        )
        self.trades.append(trade)

        return {
            "status": "FILLED",
            "trade_id": len(self.trades),
            "market_id": market_id,
            "side": side,
            "amount": amount,
            "price": price,
            "cost": cost,
            "balance": self.balance,
        }

    def get_balance(self) -> float:
        """Get current balance."""
        return self.balance

    def get_positions(self) -> list[dict[str, Any]]:
        """Get current positions."""
        return [
            {"market_id": k, **v}
            for k, v in self.positions.items()
        ]

    def get_trade_history(self) -> list[dict[str, Any]]:
        """Get trade history."""
        return [
            {
                "trade_id": i + 1,
                "market_id": t.market_id,
                "side": t.side,
                "amount": t.amount,
                "price": t.price,
                "timestamp": t.timestamp.isoformat(),
                "status": t.status,
            }
            for i, t in enumerate(self.trades)
        ]

    def get_total_pnl(self) -> float:
        """Calculate total P&L."""
        return self.balance - self.initial_balance
