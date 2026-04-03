import yfinance
from datetime import datetime
from decimal import Decimal
from typing import Optional

from apps.apis.config import YAHOO_FINANCE_ENABLED
from apps.apis.exceptions import ProviderUnavailable
from apps.apis.services.base import PriceResult, PriceService


STOCK_SYMBOLS = ["AAPL", "TSLA"]


class YahooFinanceService(PriceService):
    def get_price(self, symbol: str) -> Optional[PriceResult]:
        if not YAHOO_FINANCE_ENABLED:
            return None

        symbol = symbol.upper()
        if symbol not in STOCK_SYMBOLS:
            return None

        try:
            ticker = yfinance.Ticker(symbol)
            info = ticker.info
            price = info.get("currentPrice") or info.get("regularMarketPreviousClose")
            if price is None:
                return None
            return PriceResult(
                symbol=symbol,
                price=Decimal(str(price)),
                currency="USD",
                provider="yahoo",
                timestamp=datetime.utcnow(),
            )
        except Exception as e:
            raise ProviderUnavailable(f"Yahoo Finance API failed: {e}")

    def get_all_prices(self) -> dict[str, PriceResult]:
        if not YAHOO_FINANCE_ENABLED:
            return {}

        result = {}
        for symbol in STOCK_SYMBOLS:
            price_result = self.get_price(symbol)
            if price_result:
                result[symbol] = price_result
        return result
