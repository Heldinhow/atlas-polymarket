"""Layer 3: Aschenbrenner-inspired agent - narrative identification."""
from typing import Any
from src.agents.base import BaseAgent


class AschenbrennerAgent(BaseAgent):
    """Narrative identification agent inspired by Luke Aschenbrenner."""

    def __init__(self):
        super().__init__(
            name="AschenbrennerBot",
            role="Narrative analyst identifying high-impact market narratives",
        )

    async def build_position(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build position based on narrative analysis."""
        prompt = f"""As Aschenbrenner, identify the narrative:

Market: {context.get('market')}
Current Narrative: {context.get('current_narrative')}
Sentiment: {context.get('sentiment')}
Trend Acceleration: {context.get('trend_acceleration')}

Provide:
1. Narrative assessment
2. How to position
3. Narrative longevity (Short/Medium/Long)
4. Conviction (1-10)
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "market": context.get("market"),
            "position": response,
            "conviction": self._extract_conviction(response),
            "type": "narrative",
        }

    def _extract_conviction(self, response: str) -> int:
        """Extract conviction level."""
        import re
        match = re.search(r"conviction[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5