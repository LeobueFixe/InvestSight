from datetime import datetime
from decimal import Decimal
from typing import Optional

from apps.apis.services.base import PriceResult, PriceService


MOCK_PRICES = {
    "BTC": Decimal("67500.00"),
    "ETH": Decimal("3450.00"),
    "AAPL": Decimal("175.50"),
    "TSLA": Decimal("250.00"),
}


class MockPriceService(PriceService):
    def get_price(self, symbol: str) -> Optional[PriceResult]:
        symbol = symbol.upper()
        if symbol not in MOCK_PRICES:
            return None
        return PriceResult(
            symbol=symbol,
            price=MOCK_PRICES[symbol],
            currency="USD",
            provider="mock",
            timestamp=datetime.utcnow(),
        )

    def get_all_prices(self) -> dict[str, PriceResult]:
        return {symbol: self.get_price(symbol) for symbol in MOCK_PRICES}
