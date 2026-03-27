import os
import environ

env = environ.Env()

USE_MOCK_DATA = env("USE_MOCK_DATA", default=True)

COINGECKO_BASE_URL = env(
    "COINGECKO_BASE_URL", default="https://api.coingecko.com/api/v3"
)
COINGECKO_API_KEY = env("COINGECKO_API_KEY", default="")

YAHOO_FINANCE_ENABLED = env("YAHOO_FINANCE_ENABLED", default=False)

CACHE_TTL_CRYPTO = env("CACHE_TTL_CRYPTO", default=300)
CACHE_TTL_STOCK = env("CACHE_TTL_STOCK", default=600)

RETRY_MAX_ATTEMPTS = env("RETRY_MAX_ATTEMPTS", default=3)

LOG_LEVEL = env("LOG_LEVEL", default="DEBUG")

PROVIDER_REGISTRY = {
    "BTC": "coingecko",
    "ETH": "coingecko",
    "AAPL": "yahoo",
    "TSLA": "yahoo",
}
