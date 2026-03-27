import pytest
from decimal import Decimal

from apps.portfolio.models import Alert


class TestAlerts:
    def test_alert_str(self):
        from django.contrib.auth.models import User
        from apps.portfolio.models import Portfolio
        from apps.wallet.models import Asset, AssetType

        user = User(username="test", email="test@test.com")
        portfolio = Portfolio(name="Test", user=user)
        asset = Asset(symbol="BTC", name="Bitcoin", asset_type=AssetType.CRYPTO)

        alert = Alert(
            portfolio=portfolio,
            asset=asset,
            target_price=Decimal("70000.00"),
            direction="above",
        )
        assert "BTC" in str(alert)
        assert "above" in str(alert)

    def test_alert_index(self):
        indexes = [idx.fields for idx in Alert._meta.indexes]
        assert ["portfolio", "active"] in indexes
