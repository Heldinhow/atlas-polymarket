"""Layer 4: CIO Synthesis - final synthesis of all agent outputs."""
from typing import Any
from src.agents.base import BaseAgent


class CIOSynthesisAgent(BaseAgent):
    """Chief Investment Officer synthesis of all layer outputs."""

    def __init__(self):
        super().__init__(
            name="CIOSynthesis",
            role="Chief Investment Officer synthesizing all agent analysis into final decision",
        )

    async def synthesize(
        self,
        layer1_output: dict[str, Any],
        layer2_output: dict[str, Any],
        layer3_output: dict[str, Any],
    ) -> dict[str, Any]:
        """Synthesize all layer outputs into a final recommendation."""
        prompt = f"""As CIO, synthesize all agent outputs:

Layer 1 (Macro): {layer1_output}
Layer 2 (Sector): {layer2_output}
Layer 3 (Superinvestors): {layer3_output}

Provide:
1. Final market assessment
2. Recommended action (BUY/SELL/HOLD)
3. Confidence in decision (1-10)
4. Key rationale
"""
        response = await self.think(prompt)

        return {
            "agent": self.name,
            "synthesis": response,
            "action": self._extract_action(response),
            "confidence": self._extract_confidence(response),
        }

    def _extract_action(self, response: str) -> str:
        """Extract action from response."""
        response_upper = response.upper()
        if "BUY" in response_upper:
            return "BUY"
        elif "SELL" in response_upper:
            return "SELL"
        return "HOLD"

    def _extract_confidence(self, response: str) -> int:
        """Extract confidence level."""
        import re
        match = re.search(r"confidence[:\s]+(\d)", response, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5
