"""Tests for EsportsMacroAgent."""
import pytest
from unittest.mock import AsyncMock, patch


class TestEsportsMacroAgent:
    """Tests for EsportsMacroAgent."""

    @pytest.fixture
    def agent(self):
        from src.agents.layer1.esports_macro import EsportsMacroAgent
        return EsportsMacroAgent()

    @pytest.mark.asyncio
    async def test_agent_name(self, agent):
        """Agent should have correct name."""
        assert agent.name == "EsportsMacro"

    @pytest.mark.asyncio
    async def test_analyze_returns_dict(self, agent):
        """Analyze should return a dict with analysis."""
        with patch.object(agent, "think", new_callable=AsyncMock) as mock_think:
            mock_think.return_value = "Bull market for esports"
            context = {"markets": []}

            result = await agent.analyze(context)
            assert isinstance(result, dict)