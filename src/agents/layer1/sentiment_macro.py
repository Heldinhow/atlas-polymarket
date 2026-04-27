"""Layer 1: Sentiment Macro Agent - analyzes social/narrative sentiment."""
from typing import Any
from src.agents.base import BaseAgent


class SentimentMacroAgent(BaseAgent):
    """Analyzes social media sentiment and narratives around teams/players."""

    def __init__(self):
        super().__init__(
            name="SentimentMacro",
            role="Analyst of social sentiment, narratives, and market psychology",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze market sentiment and narratives."""
        prompt = f"""Analyze current market sentiment based on:

Social Mentions: {context.get('social_mentions', [])}
News Headlines: {context.get('news_headlines', [])}
Narrative Shifts: {context.get('narrative_shifts', [])}

Provide a brief analysis of:
1. Overall market sentiment (bullish/bearish/neutral)
2. Dominant narratives
3. Sentiment risks
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "regime": self._extract_regime(response),
            "analysis": response,
            "confidence": 0.6,
        }

    def _extract_regime(self, response: str) -> str:
        """Extract sentiment from response."""
        response_lower = response.lower()
        if "bullish" in response_lower:
            return "BULL"
        elif "bearish" in response_lower:
            return "BEAR"
        elif "crisis" in response_lower or "panic" in response_lower:
            return "CRISIS"
        return "NEUTRAL"