"""Layer 4: CRO Agent - risk management and position sizing."""
from typing import Any
from src.agents.base import BaseAgent


class CROAgent(BaseAgent):
    """Chief Risk Officer - manages risk and position sizing."""

    def __init__(self):
        super().__init__(
            name="CRO",
            role="Chief Risk Officer managing portfolio risk and position sizing",
        )

    async def assess_risk(self, context: dict[str, Any]) -> dict[str, Any]:
        """Assess risk for proposed position."""
        prompt = f"""Assess risk for this position:

Proposed Position: {context.get('position')}
Portfolio Value: {context.get('portfolio_value')}
Existing Positions: {context.get('existing_positions', [])}
Market Volatility: {context.get('volatility', 'medium')}

Provide:
1. Position sizing recommendation
2. Stop loss level
3. Risk score (1-10, 10 = highest risk)
4. Max loss acceptable
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "risk_assessment": response,
            "position_size": self._extract_size(response),
            "stop_loss": self._extract_stop_loss(response),
            "risk_score": self._extract_risk_score(response),
        }

    def _extract_size(self, response: str) -> str:
        """Extract position size recommendation."""
        import re
        match = re.search(r"(\d+%)", response)
        if match:
            return match.group(1)
        return "5%"

    def _extract_stop_loss(self, response: str) -> str:
        """Extract stop loss level."""
        import re
        match = re.search(r"stop loss[:\s]+([\d.]+)", response, re.IGNORECASE)
        if match:
            return match.group(1)
        return "0.0"

    def _extract_risk_score(self, response: str) -> int:
        """Extract risk score."""
        import re
        match = re.search(r"risk[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5
