"""Tests for DruckenmillerAgent."""
import pytest
from unittest.mock import AsyncMock, patch


class TestDruckenmillerAgent:
    """Tests for DruckenmillerAgent."""

    @pytest.fixture
    def agent(self):
        from src.agents.layer3.druckenmiller import DruckenmillerAgent
        return DruckenmillerAgent()

    @pytest.mark.asyncio
    async def test_agent_name(self, agent):
        """Agent should have correct name."""
        assert agent.name == "DruckenmillerBot"

    @pytest.mark.asyncio
    async def test_build_position_returns_dict(self, agent):
        """Build position should return position recommendation."""
        with patch.object(agent, "think", new_callable=AsyncMock) as mock_think:
            mock_think.return_value = "Buy 5% position"
            context = {"market": "test", "analysis": "bullish"}

            result = await agent.build_position(context)
            assert isinstance(result, dict)