"""Tests for EarningsDeskAgent."""
import pytest
from unittest.mock import AsyncMock, patch


class TestEarningsDeskAgent:
    """Tests for EarningsDeskAgent."""

    @pytest.fixture
    def agent(self):
        from src.agents.layer2.earnings_desk import EarningsDeskAgent
        return EarningsDeskAgent()

    @pytest.mark.asyncio
    async def test_agent_name(self, agent):
        """Agent should have correct name."""
        assert agent.name == "EarningsDesk"

    @pytest.mark.asyncio
    async def test_analyze_returns_dict(self, agent):
        """Analyze should return sector analysis."""
        with patch.object(agent, "think", new_callable=AsyncMock) as mock_think:
            mock_think.return_value = "Team A has good recent form"
            context = {"team": "Team A", "history": []}

            result = await agent.analyze(context)
            assert isinstance(result, dict)