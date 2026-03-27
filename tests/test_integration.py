import pytest
from decimal import Decimal


@pytest.mark.django_db
class TestIntegration:
    def test_create_portfolio_and_holding(self):
        from django.contrib.auth.models import User
        from apps.wallet.models import Asset, AssetType
        from apps.portfolio.models import Portfolio
        from apps.wallet.models import Holding

        user = User.objects.create_user(username="testuser", password="testpass")
        asset = Asset.objects.create(
            symbol="BTC", name="Bitcoin", asset_type=AssetType.CRYPTO
        )
        portfolio = Portfolio.objects.create(name="Test Portfolio", user=user)

        holding = Holding.objects.create(
            portfolio=portfolio,
            asset=asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )

        assert holding.id is not None
        assert holding.total_cost == Decimal("50000.00")

    def test_portfolio_aggregation(self):
        from django.contrib.auth.models import User
        from apps.wallet.models import Asset, AssetType
        from apps.portfolio.models import Portfolio
        from apps.wallet.models import Holding

        user = User.objects.create_user(username="testuser2", password="testpass2")
        asset = Asset.objects.create(
            symbol="BTC", name="Bitcoin", asset_type=AssetType.CRYPTO
        )
        portfolio = Portfolio.objects.create(name="Test Portfolio 2", user=user)

        Holding.objects.create(
            portfolio=portfolio,
            asset=asset,
            quantity=Decimal("1.0"),
            avg_buy_price=Decimal("50000.00"),
        )

        assert portfolio.total_invested > 0
