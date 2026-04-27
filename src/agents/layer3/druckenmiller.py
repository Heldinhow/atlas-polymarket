"""Layer 3: Druckenmiller-inspired agent - macro positioning."""
from typing import Any
from src.agents.base import BaseAgent


class DruckenmillerAgent(BaseAgent):
    """Macro positioning agent inspired by Stanley Druckenmiller."""

    def __init__(self):
        super().__init__(
            name="DruckenmillerBot",
            role="Macro trader focused on big trends and high-conviction positions",
        )

    async def build_position(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build a macro-inspired position."""
        prompt = f"""As Druckenmiller, analyze this position opportunity:

Market: {context.get('market')}
Macro Regime: {context.get('macro_regime')}
Sector Analysis: {context.get('sector_analysis')}
Risk/Reward: {context.get('risk_reward')}

Provide:
1. Position sizing (as % of portfolio)
2. Entry strategy
3. Exit strategy
4. Conviction level (1-10)
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "market": context.get("market"),
            "position": response,
            "conviction": self._extract_conviction(response),
            "type": "macro",
        }

    def _extract_conviction(self, response: str) -> int:
        """Extract conviction level from response."""
        import re
        match = re.search(r"conviction[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5