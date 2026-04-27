"""Tests for Polymarket API client."""
import pytest
from unittest.mock import AsyncMock, patch


class TestPolymarketClient:
    """Tests for Polymarket API client."""

    @pytest.fixture
    def client(self):
        from src.data.polymarket_client import PolymarketClient
        return PolymarketClient(api_key="test_key")

    @pytest.mark.asyncio
    async def test_get_markets_returns_list(self, client):
        """Should return list of markets."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"markets": []}
            mock_get.return_value = mock_response

            result = await client.get_markets(category="esports")
            assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_market_price(self, client):
        """Should return price for a market."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.json.return_value = {"price": "0.55"}
            mock_get.return_value = mock_response

            result = await client.get_market_price("test-market-id")
            assert result == "0.55"
