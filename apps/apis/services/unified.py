from typing import Optional

from apps.apis.config import PROVIDER_REGISTRY, USE_MOCK_DATA
from apps.apis.services.base import PriceResult
from apps.apis.services.mock import MockPriceService
from apps.apis.services.coingecko import CoinGeckoService
from apps.apis.services.yahoo import YahooFinanceService


class UnifiedPriceService:
    def __init__(self):
        self.mock_service = MockPriceService()
        self.coingecko_service = CoinGeckoService()
        self.yahoo_service = YahooFinanceService()

    def get_price(self, symbol: str) -> Optional[PriceResult]:
        if USE_MOCK_DATA:
            return self.mock_service.get_price(symbol)

        symbol = symbol.upper()
        provider = PROVIDER_REGISTRY.get(symbol)

        if provider == "coingecko":
            try:
                return self.coingecko_service.get_price(symbol)
            except Exception:
                return self.mock_service.get_price(symbol)
        elif provider == "yahoo":
            try:
                return self.yahoo_service.get_price(symbol)
            except Exception:
                return self.mock_service.get_price(symbol)

        return self.mock_service.get_price(symbol)

    def get_all_prices(self) -> dict[str, PriceResult]:
        if USE_MOCK_DATA:
            return self.mock_service.get_all_prices()

        result = {}
        try:
            result.update(self.coingecko_service.get_all_prices())
        except Exception:
            pass

        try:
            result.update(self.yahoo_service.get_all_prices())
        except Exception:
            pass

        for symbol in PROVIDER_REGISTRY:
            if symbol not in result:
                mock_result = self.mock_service.get_price(symbol)
                if mock_result:
                    result[symbol] = mock_result

        return result


_unified_service = None


def get_price(symbol: str) -> Optional[PriceResult]:
    global _unified_service
    if _unified_service is None:
        _unified_service = UnifiedPriceService()
    return _unified_service.get_price(symbol)


def get_all_prices() -> dict[str, PriceResult]:
    global _unified_service
    if _unified_service is None:
        _unified_service = UnifiedPriceService()
    return _unified_service.get_all_prices()
