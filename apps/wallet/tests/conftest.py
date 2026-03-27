import pytest
from decimal import Decimal


@pytest.fixture
def asset_btc():
    from apps.wallet.models import Asset

    return Asset(symbol="BTC", name="Bitcoin", asset_type="crypto")


@pytest.fixture
def asset_eth():
    from apps.wallet.models import Asset

    return Asset(symbol="ETH", name="Ethereum", asset_type="crypto")


@pytest.fixture
def asset_aapl():
    from apps.wallet.models import Asset

    return Asset(symbol="AAPL", name="Apple Inc.", asset_type="stock")
