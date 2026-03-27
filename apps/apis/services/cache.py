from datetime import date
from typing import Optional

from django.core.cache import cache

from apps.apis.config import CACHE_TTL_CRYPTO, CACHE_TTL_STOCK, PROVIDER_REGISTRY
from apps.apis.services.base import PriceResult
from apps.apis.services.unified import UnifiedPriceService


_unified_service = None


def _get_unified_service():
    global _unified_service
    if _unified_service is None:
        _unified_service = UnifiedPriceService()
    return _unified_service


def _get_cache_ttl(symbol: str) -> int:
    provider = PROVIDER_REGISTRY.get(symbol.upper(), "mock")
    if provider == "coingecko":
        return CACHE_TTL_CRYPTO
    elif provider == "yahoo":
        return CACHE_TTL_STOCK
    return 300


def _make_cache_key(symbol: str) -> str:
    today = date.today().isoformat()
    return f"price:{symbol.upper()}:{today}"


def get_cached_price(symbol: str) -> Optional[PriceResult]:
    cache_key = _make_cache_key(symbol)
    cached = cache.get(cache_key)
    if cached:
        return cached
    return None


def set_cached_price(symbol: str, price_result: PriceResult) -> None:
    cache_key = _make_cache_key(symbol)
    ttl = _get_cache_ttl(symbol)
    cache.set(cache_key, price_result, ttl)


def get_price_with_cache(symbol: str) -> Optional[PriceResult]:
    cached = get_cached_price(symbol)
    if cached:
        return cached

    price_result = _get_unified_service().get_price(symbol)
    if price_result:
        set_cached_price(symbol, price_result)

    return price_result
