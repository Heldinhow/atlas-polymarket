"""Layer 4: Alpha Discovery - identifies unexplored opportunities."""
from typing import Any
from src.agents.base import BaseAgent


class AlphaDiscoveryAgent(BaseAgent):
    """Discovers untapped alpha opportunities in the market."""

    def __init__(self):
        super().__init__(
            name="AlphaDiscovery",
            role="Alpha researcher finding unexplored market opportunities",
        )

    async def find_alpha(self, context: dict[str, Any]) -> dict[str, Any]:
        """Find unexplored alpha opportunities."""
        prompt = f"""Find alpha opportunities:

Active Markets: {context.get('markets', [])}
Existing Positions: {context.get('positions', [])}
Market Gaps: {context.get('gaps', [])}

Provide:
1. New alpha opportunities
2. Why they are unexplored
3. Potential edge
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "alpha_opportunities": response,
            "count": self._count_opportunities(response),
        }

    def _count_opportunities(self, response: str) -> int:
        """Count alpha opportunities mentioned."""
        import re
        matches = re.findall(r"\d+\.", response)
        return len(matches)
