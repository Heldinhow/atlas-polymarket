"""Soros Reflexivity Engine: models market feedback loops."""
from typing import Any


class SorosEngine:
    """Models market feedback loops including Price→Fundamentals, P&L→Behavior."""

    def __init__(self):
        self.price_history: list[float] = []
        self.pnl_history: list[float] = []

    def add_price(self, price: float) -> None:
        """Add price point to history."""
        self.price_history.append(price)
        if len(self.price_history) > 100:
            self.price_history = self.price_history[-100:]

    def add_pnl(self, pnl: float) -> None:
        """Add P&L to history."""
        self.pnl_history.append(pnl)
        if len(self.pnl_history) > 50:
            self.pnl_history = self.pnl_history[-50:]

    def detect_reflexivity(self) -> dict[str, Any]:
        """Detect reflexive feedback loops.

        Returns:
            dict with reflexivity signals
        """
        price_trend = self._get_price_trend()
        pnl_trend = self._get_pnl_trend()
        narrative = self._detect_narrative()

        return {
            "price_fundamentals_feedback": self._price_fundamentals(price_trend),
            "pnl_behavior_feedback": self._pnl_behavior(pnl_trend),
            "narrative_flows": narrative,
            "reflexivity_score": self._compute_reflexivity_score(
                price_trend, pnl_trend, narrative
            ),
        }

    def _get_price_trend(self) -> str:
        """Get recent price trend."""
        if len(self.price_history) < 5:
            return "neutral"
        recent = self.price_history[-5:]
        if recent[-1] > recent[0] * 1.05:
            return "up"
        elif recent[-1] < recent[0] * 0.95:
            return "down"
        return "neutral"

    def _get_pnl_trend(self) -> str:
        """Get recent P&L trend."""
        if len(self.pnl_history) < 3:
            return "neutral"
        recent = self.pnl_history[-3:]
        if sum(recent) > 0:
            return "profitable"
        elif sum(recent) < 0:
            return "losing"
        return "neutral"

    def _detect_narrative(self) -> str:
        """Detect current narrative."""
        if len(self.price_history) < 10:
            return "forming"

        trend = self._get_price_trend()
        if trend == "up":
            return "bullish_narrative"
        elif trend == "down":
            return "bearish_narrative"
        return "uncertain"

    def _price_fundamentals(self, trend: str) -> str:
        """Price→Fundamentals feedback loop."""
        if trend == "up":
            return "Self-reinforcing: rising prices attract more buying"
        elif trend == "down":
            return "Self-defeating: falling prices trigger selling"
        return "Balanced"

    def _pnl_behavior(self, trend: str) -> str:
        """P&L→Behavior feedback loop."""
        if trend == "profitable":
            return "Risk-on: profits encourage larger positions"
        elif trend == "losing":
            return "Risk-off: losses trigger position reduction"
        return "Neutral"

    def _compute_reflexivity_score(
        self, price_trend: str, pnl_trend: str, narrative: str
    ) -> float:
        """Compute overall reflexivity score (0-1)."""
        score = 0.0
        if price_trend != "neutral":
            score += 0.3
        if pnl_trend != "neutral":
            score += 0.3
        if narrative in ("bullish_narrative", "bearish_narrative"):
            score += 0.4
        return min(score, 1.0)
