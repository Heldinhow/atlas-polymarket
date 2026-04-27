"""Layer 2: Schedule Desk - analyzes game schedules, fatigue, and travel factors."""
from typing import Any
from src.agents.base import BaseAgent


class ScheduleDeskAgent(BaseAgent):
    """Analyzes game schedules, fatigue, and travel factors."""

    def __init__(self):
        super().__init__(
            name="ScheduleDesk",
            role="Analyst of game schedules, team fatigue, and travel impact",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze schedule and fatigue factors."""
        prompt = f"""Analyze schedule and fatigue factors:

Team: {context.get('team', 'Unknown')}
Games Last 7 Days: {context.get('games_last_7_days', 0)}
Games Last 14 Days: {context.get('games_last_14_days', 0)}
Travel Distance: {context.get('travel_distance', 'Unknown')}
Time Zone Changes: {context.get('tz_changes', 0)}

Provide:
1. Fatigue assessment
2. Schedule impact on performance
3. Risk level (Low/Medium/High)
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "team": context.get("team"),
            "analysis": response,
            "fatigue_risk": self._extract_risk(response),
            "confidence": 0.65,
        }

    def _extract_risk(self, response: str) -> str:
        """Extract risk level from response."""
        response_lower = response.lower()
        if "high" in response_lower:
            return "HIGH"
        elif "medium" in response_lower:
            return "MEDIUM"
        return "LOW"