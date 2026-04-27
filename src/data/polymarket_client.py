"""Polymarket API client for fetching markets, prices, and volumes."""
import httpx
from typing import Any


class PolymarketClient:
    """Client for interacting with Polymarket CLOB API."""

    def __init__(self, api_key: str, base_url: str | None = None):
        self.api_key = api_key
        self.base_url = base_url or "https://clob.polymarket.com"
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Lazy initialization of HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0,
            )
        return self._client

    async def get_markets(
        self, category: str | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Fetch list of markets, optionally filtered by category."""
        client = await self._get_client()
        params = {"limit": limit}
        if category:
            params["category"] = category

        response = await client.get("/markets", params=params)
        response.raise_for_status()
        data = response.json()
        # Polymarket returns data in "data" field
        return data.get("data", [])

    async def get_market_price(self, market_id: str) -> str:
        """Get current price for a specific market."""
        client = await self._get_client()
        response = await client.get(f"/markets/{market_id}")
        response.raise_for_status()
        data = response.json()
        return data.get("price", "0.0")

    async def get_market_volume(self, market_id: str) -> float:
        """Get 24h volume for a specific market."""
        client = await self._get_client()
        response = await client.get(f"/markets/{market_id}/volume")
        response.raise_for_status()
        data = response.json()
        return float(data.get("volume", 0.0))

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
