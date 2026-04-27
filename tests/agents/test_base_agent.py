"""Tests for BaseAgent class."""
import pytest
from unittest.mock import AsyncMock, patch


class TestBaseAgent:
    """Tests for BaseAgent class."""

    @pytest.fixture
    def agent(self):
        from src.agents.base import BaseAgent
        return BaseAgent(name="TestAgent", role="testing")

    @pytest.mark.asyncio
    async def test_agent_has_name(self, agent):
        """Agent should have a name."""
        assert agent.name == "TestAgent"

    @pytest.mark.asyncio
    async def test_agent_has_role(self, agent):
        """Agent should have a role."""
        assert agent.role == "testing"

    @pytest.mark.asyncio
    async def test_think_returns_string(self, agent):
        """Think method should return a string."""
        with patch("src.core.llm.MinimaxClient", create=True) as mock_client:
            mock_instance = AsyncMock()
            mock_instance.complete.return_value = "Test response"
            mock_client.return_value = mock_instance

            result = await agent.think("Test prompt")
            assert isinstance(result, str)