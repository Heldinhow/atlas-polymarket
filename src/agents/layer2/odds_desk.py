"""Layer 2: Odds Desk - compares Polymarket odds with external sportsbooks."""
from typing import Any
from src.agents.base import BaseAgent


class OddsDeskAgent(BaseAgent):
    """Compares Polymarket odds with external sportsbooks to find arbitrage."""

    def __init__(self):
        super().__init__(
            name="OddsDesk",
            role="Analyst comparing Polymarket odds with external sportsbooks",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze odds discrepancies."""
        prompt = f"""Analyze odds comparison:

Polymarket Odds: {context.get('polymarket_odds', {})}
External Odds: {context.get('external_odds', {})}
Market ID: {context.get('market_id', 'Unknown')}

Provide:
1. Odds discrepancy analysis
2. Arbitrage opportunity (if any)
3. Confidence in the edge
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "market_id": context.get("market_id"),
            "analysis": response,
            "confidence": 0.8,
        }