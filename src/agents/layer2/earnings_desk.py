"""Layer 2: Earnings Desk - analyzes team/player performance and head-to-head records."""
from typing import Any
from src.agents.base import BaseAgent


class EarningsDeskAgent(BaseAgent):
    """Analyzes team performance, head-to-head records, and recent form."""

    def __init__(self):
        super().__init__(
            name="EarningsDesk",
            role="Analyst of team performance, head-to-head records, and recent form",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze team/sector performance."""
        prompt = f"""Analyze the team performance based on:

Team: {context.get('team', 'Unknown')}
Recent Form: {context.get('recent_form', [])}
Head-to-Head: {context.get('h2h', [])}
Home/Away: {context.get('home_away', {})}

Provide:
1. Performance assessment
2. Key factors for this matchup
3. Risk factors
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "team": context.get("team"),
            "analysis": response,
            "confidence": 0.75,
        }