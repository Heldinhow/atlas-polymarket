"""Tests for PRISM market regime detection."""
import pytest
from src.core.prism import PRISM, MarketRegime


class TestPRISM:
    """Tests for PRISM market regime detection."""

    @pytest.fixture
    def prism(self):
        return PRISM()

    def test_detect_regime_returns_enum(self, prism):
        """Should return a MarketRegime enum value."""
        context = {"volume": 1000000, "volatility": "high", "sentiment": "fear"}
        result = prism.detect_regime(context)
        assert isinstance(result, MarketRegime)

    def test_bull_regime(self, prism):
        """Should detect bull/low vol regime."""
        context = {"volume": 500000, "volatility": "low", "sentiment": "bullish"}
        result = prism.detect_regime(context)
        assert result == MarketRegime.BULL_LOW_VOL
