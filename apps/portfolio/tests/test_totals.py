import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from apps.portfolio.models import Portfolio


class TestPortfolioTotals:
    @patch("apps.portfolio.models.Portfolio.holdings")
    def test_total_invested(self, mock_holdings):
        from django.contrib.auth.models import User

        user = User(username="test", email="test@test.com")
        portfolio = Portfolio(name="Test", user=user)

        mock_qs = MagicMock()
        mock_qs.aggregate.return_value = {"total": Decimal("100000.00")}
        mock_holdings.return_value = mock_qs

        assert portfolio.total_invested == Decimal("100000.00")

    @patch("apps.portfolio.models.Portfolio.holdings")
    def test_total_invested_none(self, mock_holdings):
        from django.contrib.auth.models import User

        user = User(username="test", email="test@test.com")
        portfolio = Portfolio(name="Test", user=user)

        mock_qs = MagicMock()
        mock_qs.aggregate.return_value = {"total": None}
        mock_holdings.return_value = mock_qs

        assert portfolio.total_invested == Decimal("0")

    @patch("apps.portfolio.models.Portfolio.holdings")
    def test_current_value_empty(self, mock_holdings):
        from django.contrib.auth.models import User

        user = User(username="test", email="test@test.com")
        portfolio = Portfolio(name="Test", user=user)

        mock_qs = MagicMock()
        mock_qs.select_related.return_value = []
        mock_holdings.return_value = mock_qs

        assert portfolio.current_value == Decimal("0")
