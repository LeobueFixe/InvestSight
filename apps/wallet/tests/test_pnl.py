import pytest
from decimal import Decimal
from unittest.mock import MagicMock

from apps.wallet.models import Holding


class TestPnL:
    @pytest.fixture
    def mock_asset(self):
        asset = MagicMock()
        asset.symbol = "BTC"
        asset.current_price = Decimal("67500.00")
        return asset

    @pytest.fixture
    def mock_portfolio(self):
        portfolio = MagicMock()
        portfolio.id = 1
        return portfolio

    def test_profit_loss_gain(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.profit_loss == Decimal("17500.00")

    def test_profit_loss_loss(self, mock_asset, mock_portfolio):
        mock_asset.current_price = Decimal("40000.00")
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.profit_loss == Decimal("-10000.00")

    def test_profit_loss_breakeven(self, mock_asset, mock_portfolio):
        mock_asset.current_price = Decimal("50000.00")
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.profit_loss == Decimal("0")

    def test_pnl_pct_gain(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.pnl_pct == Decimal("35")

    def test_pnl_pct_zero_cost(self, mock_asset, mock_portfolio):
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("0"),
            avg_buy_price=Decimal("0"),
        )
        assert holding.pnl_pct is None

    def test_pnl_pct_none_when_current_value_none(self, mock_asset, mock_portfolio):
        mock_asset.current_price = None
        holding = Holding(
            portfolio=mock_portfolio,
            asset=mock_asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )
        assert holding.pnl_pct is None
