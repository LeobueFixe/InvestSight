import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from apps.wallet.models import Holding, Asset, AssetType


class TestHolding:
    @pytest.fixture
    def mock_asset(self):
        asset = MagicMock(spec=Asset)
        asset.symbol = "BTC"
        asset.current_price = Decimal("67500.00")
        return asset

    @pytest.fixture
    def mock_portfolio(self):
        portfolio = MagicMock()
        portfolio.id = 1
        return portfolio

    def test_holding_str(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.5"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert "BTC" in str(holding)

    def test_total_cost(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("2.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.total_cost == Decimal("100000.00")

    def test_current_value(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.current_value == Decimal("67500.00")

    def test_current_value_no_price(self, mock_asset, mock_portfolio):
        mock_asset.current_price = None
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.current_value is None
