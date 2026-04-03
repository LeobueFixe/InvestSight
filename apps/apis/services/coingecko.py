import requests
from datetime import datetime
from decimal import Decimal
from typing import Optional

from apps.apis.config import COINGECKO_BASE_URL, COINGECKO_API_KEY
from apps.apis.exceptions import ProviderUnavailable
from apps.apis.services.base import PriceResult, PriceService


COINGECKO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
}


class CoinGeckoService(PriceService):
    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
        self.api_key = COINGECKO_API_KEY

    def get_price(self, symbol: str) -> Optional[PriceResult]:
        symbol = symbol.upper()
        if symbol not in COINGECKO_IDS:
            return None

        coin_id = COINGECKO_IDS[symbol]
        url = f"{self.base_url}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
        }
        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get(coin_id, {}).get("usd")
            if price is None:
                return None
            return PriceResult(
                symbol=symbol,
                price=Decimal(str(price)),
                currency="USD",
                provider="coingecko",
                timestamp=datetime.utcnow(),
            )
        except requests.RequestException as e:
            raise ProviderUnavailable(f"CoinGecko API failed: {e}")

    def get_all_prices(self) -> dict[str, PriceResult]:
        if not self.base_url:
            return {}

        url = f"{self.base_url}/simple/price"
        params = {
            "ids": ",".join(COINGECKO_IDS.values()),
            "vs_currencies": "usd",
        }
        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            result = {}
            for symbol, coin_id in COINGECKO_IDS.items():
                if coin_id in data:
                    price = data[coin_id].get("usd")
                    if price:
                        result[symbol] = PriceResult(
                            symbol=symbol,
                            price=Decimal(str(price)),
                            currency="USD",
                            provider="coingecko",
                            timestamp=datetime.utcnow(),
                        )
            return result
        except requests.RequestException as e:
            raise ProviderUnavailable(f"CoinGecko API failed: {e}")
