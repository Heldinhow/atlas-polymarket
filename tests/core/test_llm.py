"""Tests for MiniMax LLM client."""
import pytest
from unittest.mock import AsyncMock, MagicMock
import sys


class TestMinimaxClient:
    """Tests for MiniMax LLM client."""

    @pytest.fixture
    def client(self):
        mock_settings = MagicMock()
        mock_settings.minimax_api_key = "test_key"

        # Create a mock config module
        mock_config_module = MagicMock()
        mock_config_module.get_settings.return_value = mock_settings

        # Patch sys.modules to replace src.config
        original_modules = sys.modules.copy()
        sys.modules['src.config'] = mock_config_module

        try:
            import importlib
            if 'src.core.llm' in sys.modules:
                del sys.modules['src.core.llm']
            from src.core.llm import MinimaxClient
            c = MinimaxClient(api_key="test_key")
            return c
        finally:
            # Restore original modules
            for key in list(sys.modules.keys()):
                if key not in original_modules:
                    del sys.modules[key]

    @pytest.mark.asyncio
    async def test_complete_returns_string(self, client):
        """Complete should return a string response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"messages": [{"content": "Test response"}]}]
        }
        mock_response.raise_for_status = MagicMock()

        # Mock _get_client to return a mock HTTP client with async post
        mock_http_client = MagicMock()
        mock_http_client.post = AsyncMock(return_value=mock_response)

        mock_get_client = AsyncMock(return_value=mock_http_client)
        client._get_client = mock_get_client

        result = await client.complete("Test prompt")
        assert isinstance(result, str)
        assert result == "Test response"