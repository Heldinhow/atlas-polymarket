"""Layer 1: Esports Macro Agent - analyzes esports market trends."""
from typing import Any
from src.agents.base import BaseAgent


class EsportsMacroAgent(BaseAgent):
    """Analyzes macro trends in esports markets."""

    def __init__(self):
        super().__init__(
            name="EsportsMacro",
            role="Analyst of esports market trends, game metas, and tournament landscapes",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze esports market conditions."""
        prompt = f"""Analyze the current esports market conditions based on:

Markets: {context.get('markets', [])}
Volumes: {context.get('volumes', [])}
Recent Trends: {context.get('recent_trends', [])}

Provide a brief analysis of:
1. Current market regime (bull/bear/crisis/recovery)
2. Key trends to watch
3. Risk factors
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
        if "bull" in response_lower:
            return "BULL"
        elif "bear" in response_lower:
            return "BEAR"
        elif "crisis" in response_lower:
            return "CRISIS"
        return "NEUTRAL"