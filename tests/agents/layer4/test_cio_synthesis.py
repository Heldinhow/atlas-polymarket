"""Tests for CIOSynthesisAgent."""
import pytest
from unittest.mock import AsyncMock, patch


class TestCIOSynthesisAgent:
    """Tests for CIOSynthesisAgent."""

    @pytest.fixture
    def agent(self):
        from src.agents.layer4.cio_synthesis import CIOSynthesisAgent
        return CIOSynthesisAgent()

    @pytest.mark.asyncio
    async def test_agent_name(self, agent):
        """Agent should have correct name."""
        assert agent.name == "CIOSynthesis"

    @pytest.mark.asyncio
    async def test_synthesize_returns_dict(self, agent):
        """Synthesize should return final recommendation."""
        with patch.object(agent, "think", new_callable=AsyncMock) as mock_think:
            mock_think.return_value = "Strong buy signal"
            layer1 = {"regime": "BULL"}
            layer2 = {"analysis": "positive"}
            layer3 = {"position": "buy 10%"}

            result = await agent.synthesize(layer1, layer2, layer3)
            assert isinstance(result, dict)
