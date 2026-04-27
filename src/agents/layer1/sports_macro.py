"""Layer 1: Sports Macro Agent - analyzes sports market trends."""
from typing import Any
from src.agents.base import BaseAgent


class SportsMacroAgent(BaseAgent):
    """Analyzes macro trends in sports markets."""

    def __init__(self):
        super().__init__(
            name="SportsMacro",
            role="Analyst of sports market trends, league dynamics, and seasonal patterns",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze sports market conditions."""
        prompt = f"""Analyze the current sports market conditions based on:

Markets: {context.get('markets', [])}
Volumes: {context.get('volumes', [])}
Seasonal Factors: {context.get('seasonal_factors', [])}

Provide a brief analysis of:
1. Current market regime
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