from django.core.cache import cache
from apps.apis.services.unified import UnifiedPriceService
from apps.apis.services.base import PriceResult
from apps.apis.services.logging import get_logger
from apps.apis.settings import settings

service = UnifiedPriceService()
logger = get_logger("cache")


def get_price_with_cache(symbol: str, target_currency: str = "USD") -> PriceResult | None:
    """
    Hybrid cache:
    1. Try Django cache
    2. Try JSON file (via UnifiedPriceService)
    3. Fetch from provider
    4. Store in Django cache

    Cache key includes target_currency to avoid mixing USD/EUR/etc.
    """
    symbol = symbol.upper()
    target_currency = target_currency.upper()

    cache_key = f"price:{symbol}:{target_currency}"

    # 1. Try Django cache
    cached = cache.get(cache_key)
    if cached:
        logger.info("cache_hit", symbol=symbol, currency=target_currency)
        return cached

    logger.info("cache_miss", symbol=symbol, currency=target_currency)

    # 2. Unified service handles JSON fallback + provider + mock
    result = service.get_price(symbol, target_currency=target_currency)

    if result:
        cache.set(cache_key, result, settings.CACHE_TTL_SECONDS)
        logger.info(
            "cache_write",
            symbol=symbol,
            currency=target_currency,
            ttl=settings.CACHE_TTL_SECONDS,
        )
        return result

    logger.warning("cache_no_result", symbol=symbol)
    return None


def get_cached_price(symbol: str) -> PriceResult | None:
    """Return the cached PriceResult for a symbol (USD), or None on miss."""
    symbol = symbol.upper()
    cache_key = f"price:{symbol}:USD"
    return cache.get(cache_key)


def get_all_prices_with_cache(target_currency: str = "USD") -> dict[str, PriceResult]:
    """
    Hybrid cache for all prices.
    Cache key includes target_currency.
    """
    target_currency = target_currency.upper()
    cache_key = f"prices:all:{target_currency}"

    cached = cache.get(cache_key)
    if cached:
        logger.info("cache_hit_all_prices", currency=target_currency)
        return cached

    logger.info("cache_miss_all_prices", currency=target_currency)

    results = service.get_all_prices(target_currency=target_currency)

    cache.set(cache_key, results, settings.CACHE_TTL_SECONDS)
    logger.info(
        "cache_write_all_prices",
        count=len(results),
        currency=target_currency,
        ttl=settings.CACHE_TTL_SECONDS,
    )

    return results
