import pytest
from decimal import Decimal
from unittest.mock import patch

from apps.wallet.models import Asset, AssetType


class TestAsset:
    def test_asset_str(self):
        asset = Asset(symbol="BTC", name="Bitcoin", asset_type=AssetType.CRYPTO)
        assert str(asset) == "BTC (Bitcoin)"

    def test_asset_symbol_uppercase(self):
        asset = Asset(symbol="btc", name="Bitcoin", asset_type=AssetType.CRYPTO)
        assert asset.symbol == "btc"

    @patch("apps.wallet.models.get_price")
    def test_current_price(self, mock_get_price):
        from apps.apis.services.base import PriceResult
        from datetime import datetime

        mock_get_price.return_value = PriceResult(
            symbol="BTC",
            price=Decimal("67500.00"),
            currency="USD",
            provider="mock",
            timestamp=datetime.utcnow(),
        )

        asset = Asset(symbol="BTC", name="Bitcoin", asset_type=AssetType.CRYPTO)
        price = asset.current_price
        assert price == Decimal("67500.00")

    @patch("apps.wallet.models.get_price")
    def test_current_price_none(self, mock_get_price):
        mock_get_price.return_value = None

        asset = Asset(symbol="UNKNOWN", name="Unknown", asset_type=AssetType.CRYPTO)
        price = asset.current_price
        assert price is None
