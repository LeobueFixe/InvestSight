from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Dict, List

from apps.apis.services.base import PriceResult, PriceService


# Hard‑coded mock prices used for testing or fallback scenarios
MOCK_PRICES = {
    "BTC": Decimal("67500.00"),
    "ETH": Decimal("3450.00"),
    "AAPL": Decimal("175.50"),
    "TSLA": Decimal("250.00"),
}


class MockPriceService(PriceService):
    """
    A mock implementation of PriceService.
    Useful for development, testing, or when external providers are unavailable.
    """


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


    def get_all_prices(self) -> Dict[str, PriceResult]:
        return {
            symbol: self.get_price(symbol)
            for symbol in MOCK_PRICES
        }


    def get_history(self, symbol: str, days: int = 30) -> List[Dict]:
        """
        Returns a simple mock history:
        - last N days
        - price varies slightly each day
        """
        symbol = symbol.upper()

        if symbol not in MOCK_PRICES:
            return []

        base_price = MOCK_PRICES[symbol]
        now = datetime.utcnow()

        history = []
        for i in range(days):
            ts = int((now - timedelta(days=i)).timestamp() * 1000)
            price = float(base_price * Decimal(1 + (i * 0.001)))  # small variation

            history.append({
                "timestamp": ts,
                "price": price,
            })

        return list(reversed(history))  # oldest → newest
