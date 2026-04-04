"""
Re-exports top-level configuration constants from apps.apis.settings
so tests can do `from apps.apis import config`.
"""
from apps.apis.settings import settings

USE_MOCK_DATA = settings.USE_MOCK_DATA
PROVIDER_REGISTRY = settings.PROVIDER_REGISTRY
CACHE_TTL_CRYPTO = settings.CACHE_TTL_CRYPTO
CACHE_TTL_STOCK = settings.CACHE_TTL_STOCK
