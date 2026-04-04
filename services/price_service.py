from typing import Optional
from apps.apis.services.base import PriceResult
from apps.apis.services.cache import (
    get_price_with_cache,
    get_all_prices_with_cache
)

class PriceServiceFacade:
    def get_price(self, symbol: str) -> Optional[PriceResult]:
        return get_price_with_cache(symbol)

    def get_all_prices(self) -> dict[str, PriceResult]:
        return get_all_prices_with_cache()


_price_service = None

def get_price_service() -> PriceServiceFacade:
    global _price_service
    if _price_service is None:
        _price_service = PriceServiceFacade()
    return _price_service
