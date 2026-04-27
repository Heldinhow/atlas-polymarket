"""Layer 3: Ackman-inspired agent - high-conviction single positions."""
from typing import Any
from src.agents.base import BaseAgent


class AckmanAgent(BaseAgent):
    """High-conviction position agent inspired by Bill Ackman."""

    def __init__(self):
        super().__init__(
            name="AckmanBot",
            role="High-conviction investor focused on asymmetric opportunities",
        )

    async def build_position(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build a high-conviction position."""
        prompt = f"""As Ackman, evaluate this high-conviction opportunity:

Market: {context.get('market')}
Thesis: {context.get('thesis')}
Risk Factors: {context.get('risk_factors')}
Catalyst: {context.get('catalyst')}

Provide:
1. Position sizing (concentrated or not)
2. Investment thesis
3. Key risks
4. Conviction (1-10)
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "market": context.get("market"),
            "position": response,
            "conviction": self._extract_conviction(response),
            "type": "high_conviction",
        }

    def _extract_conviction(self, response: str) -> int:
        """Extract conviction level."""
        import re
        match = re.search(r"conviction[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5