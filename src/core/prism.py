"""PRISM: Market regime detection system."""
from enum import Enum
from typing import Any


class MarketRegime(Enum):
    """Five market regimes for PRISM training."""
    BULL_LOW_VOL = "BULL_LOW_VOL"
    CRISIS = "CRISIS"
    RATE_TIGHTENING = "RATE_TIGHTENING"
    RECOVERY = "RECOVERY"
    EUPHORIA = "EUPHORIA"


class PRISM:
    """Market regime detection across five conditions."""

    def detect_regime(self, context: dict[str, Any]) -> MarketRegime:
        """Detect current market regime from context."""
        volume = context.get("volume", 0)
        volatility = context.get("volatility", "medium")
        sentiment = context.get("sentiment", "neutral")
        price_trend = context.get("price_trend", "sideways")

        if self._is_crisis(volume, volatility, sentiment):
            return MarketRegime.CRISIS
        elif self._is_euphoria(volume, sentiment, price_trend):
            return MarketRegime.EUPHORIA
        elif self._is_recovery(volume, sentiment, price_trend):
            return MarketRegime.RECOVERY
        elif self._is_rate_tightening(volatility, price_trend):
            return MarketRegime.RATE_TIGHTENING
        else:
            return MarketRegime.BULL_LOW_VOL

    def _is_crisis(self, volume: float, volatility: str, sentiment: str) -> bool:
        """Detect crisis regime."""
        return volume > 2000000 and volatility == "high" and sentiment == "fear"

    def _is_euphoria(self, volume: float, sentiment: str, trend: str) -> bool:
        """Detect euphoria regime."""
        return volume > 1500000 and sentiment == "euphoria" and trend == "up"

    def _is_recovery(self, volume: float, sentiment: str, trend: str) -> bool:
        """Detect recovery regime."""
        return 500000 < volume < 1000000 and sentiment == "cautious" and trend == "up"

    def _is_rate_tightening(self, volatility: str, trend: str) -> bool:
        """Detect rate tightening regime."""
        return volatility == "high" and trend == "down"

    def get_regime_description(self, regime: MarketRegime) -> str:
        """Get description of regime for agent prompts."""
        descriptions = {
            MarketRegime.BULL_LOW_VOL: "Calm bull market with low volatility",
            MarketRegime.CRISIS: "High volatility crisis regime",
            MarketRegime.RATE_TIGHTENING: "Rising rates pressuring markets",
            MarketRegime.RECOVERY: "Early recovery from downturn",
            MarketRegime.EUPHORIA: "Extreme optimism with high volumes",
        }
        return descriptions.get(regime, "Unknown regime")
