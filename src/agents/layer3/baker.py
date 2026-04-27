"""Layer 3: Baker-inspired agent - quantitative analysis."""
from typing import Any
from src.agents.base import BaseAgent


class BakerAgent(BaseAgent):
    """Quantitative analysis agent inspired by quant approaches."""

    def __init__(self):
        super().__init__(
            name="BakerBot",
            role="Quantitative analyst modeling probabilities and edge",
        )

    async def build_position(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build position using quantitative analysis."""
        prompt = f"""As Baker (quant), analyze:

Market: {context.get('market')}
Historical Data: {context.get('historical_data')}
Odds: {context.get('odds')}
Volume Profile: {context.get('volume_profile')}

Provide:
1. Probability estimate
2. Edge calculation
3. Optimal position size
4. Confidence (1-10)
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "market": context.get("market"),
            "position": response,
            "conviction": self._extract_conviction(response),
            "type": "quantitative",
        }

    def _extract_conviction(self, response: str) -> int:
        """Extract confidence level."""
        import re
        match = re.search(r"confidence[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5