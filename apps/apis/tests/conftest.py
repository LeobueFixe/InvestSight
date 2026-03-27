import pytest
from decimal import Decimal


@pytest.fixture
def mock_price_btc():
    return {
        "symbol": "BTC",
        "price": Decimal("67500.00"),
        "currency": "USD",
        "provider": "mock",
    }


@pytest.fixture
def mock_price_eth():
    return {
        "symbol": "ETH",
        "price": Decimal("3450.00"),
        "currency": "USD",
        "provider": "mock",
    }
