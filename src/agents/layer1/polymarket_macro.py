"""Layer 1: Polymarket Macro Agent - analyzes Polymarket-specific trends."""
from typing import Any
from src.agents.base import BaseAgent


class PolymarketMacroAgent(BaseAgent):
    """Analyzes Polymarket platform trends and liquidity."""

    def __init__(self):
        super().__init__(
            name="PolymarketMacro",
            role="Analyst of Polymarket volume, liquidity, and platform dynamics",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze Polymarket platform conditions."""
        prompt = f"""Analyze the current Polymarket platform conditions based on:

Market Volumes: {context.get('volumes', [])}
Liquidity: {context.get('liquidity', [])}
Active Markets: {context.get('active_markets', [])}
User Activity: {context.get('user_activity', [])}

Provide a brief analysis of:
1. Current platform regime
2. Liquidity conditions
3. Opportunity assessment
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "regime": self._extract_regime(response),
            "analysis": response,
            "confidence": 0.7,
        }

    def _extract_regime(self, response: str) -> str:
        """Extract market regime from response."""
        response_lower = response.lower()
        if "bull" in response_lower or "high volume" in response_lower:
            return "BULL"
        elif "bear" in response_lower or "low volume" in response_lower:
            return "BEAR"
        elif "crisis" in response_lower:
            return "CRISIS"
        return "NEUTRAL"