import pytest
from decimal import Decimal
from datetime import date
from unittest.mock import MagicMock

from apps.portfolio.models import PortfolioSnapshot


class TestSnapshots:
    def test_snapshot_str(self):
        from django.contrib.auth.models import User
        from apps.portfolio.models import Portfolio

        user = User(username="test", email="test@test.com")
        portfolio = Portfolio(name="Test", user=user)
        snapshot = PortfolioSnapshot(
            portfolio=portfolio, date=date.today(), value=Decimal("100000.00")
        )
        assert str(snapshot) == f"Test - {date.today()}"

    def test_snapshot_unique_together(self):
        unique_together = PortfolioSnapshot._meta.unique_together
        assert ("portfolio", "date") in unique_together
