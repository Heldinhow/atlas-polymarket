"""Tests for PaperTrader."""
import pytest
from unittest.mock import AsyncMock, patch


class TestPaperTrader:
    """Tests for PaperTrader."""

    @pytest.fixture
    def trader(self):
        from src.execution.paper_trade import PaperTrader
        return PaperTrader(initial_balance=10000.0)

    def test_initial_balance(self, trader):
        """Should have correct initial balance."""
        assert trader.balance == 10000.0

    def test_place_trade(self, trader):
        """Should place a trade and update balance."""
        result = trader.place_trade(
            market_id="test_market",
            side="BUY",
            amount=100.0,
            price=0.55
        )
        assert result["status"] == "FILLED"
        assert trader.balance == 9945.0  # 10000 - (100 * 0.55)

    def test_get_positions(self, trader):
        """Should return current positions."""
        trader.place_trade("m1", "BUY", 100, 0.5)
        positions = trader.get_positions()
        assert len(positions) == 1
