"""Layer 2: Meta Desk - analyzes game meta, patch notes, and strategic trends."""
from typing import Any
from src.agents.base import BaseAgent


class MetaDeskAgent(BaseAgent):
    """Analyzes game meta, patch notes, and strategic trends."""

    def __init__(self):
        super().__init__(
            name="MetaDesk",
            role="Analyst of game meta, patch changes, and competitive strategies",
        )

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Analyze game meta and strategic factors."""
        prompt = f"""Analyze the game meta based on:

Game: {context.get('game', 'Unknown')}
Patch Notes: {context.get('patch_notes', [])}
Recent Tournament Results: {context.get('tournament_results', [])}
Meta Shifts: {context.get('meta_shifts', [])}

Provide:
1. Current meta assessment
2. Strategic implications
3. Teams that benefit from current meta
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "game": context.get("game"),
            "analysis": response,
            "confidence": 0.7,
        }