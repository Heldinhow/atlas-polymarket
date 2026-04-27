"""Tests for Autoresearch loop."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestAutoresearch:
    """Tests for Autoresearch loop."""

    @pytest.fixture
    def autoresearch(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("autoresearch", "src/core/autoresearch.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Autoresearch()

    @pytest.mark.asyncio
    async def test_identify_worst_agent(self, autoresearch):
        """Should identify worst performing agent by Sharpe."""
        with patch.object(autoresearch, "get_agent_metrics") as mock_metrics:
            mock_metrics.return_value = {
                "EsportsMacro": {"sharpe": 0.5},
                "SportsMacro": {"sharpe": 1.2},
            }
            worst = await autoresearch.identify_worst_agent()
            assert worst == "EsportsMacro"

    @pytest.mark.asyncio
    async def test_generate_prompt_modification(self, autoresearch):
        """Should generate prompt modification."""
        mock_agent = AsyncMock()
        mock_agent.prompt = "Test prompt"
        mock_agent.think.return_value = "Improved prompt"

        with patch.object(autoresearch, "_load_agent", return_value=mock_agent):
            result = await autoresearch.generate_prompt_modification(
                agent_name="TestAgent",
                performance_issue="Low Sharpe ratio"
            )
            assert isinstance(result, str)
            assert result == "Improved prompt"
