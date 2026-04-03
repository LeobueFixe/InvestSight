import json
import requests
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, List
from apps.apis.services.retry import with_retry
from apps.apis.exceptions import ProviderUnavailable
from apps.apis.services.base import PriceResult, PriceService
from apps.apis.services.logging import get_logger, log_api_call
from apps.apis.settings import settings

DATA_FILE = Path("apps/apis/data/prices.json")
logger = get_logger("coingecko")



def load_coingecko_ids() -> Dict[str, str]:
    """
    Loads CoinGecko symbol → ID mapping from data/prices.json.
    """
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {}

    return data.get("coingecko_ids", {})



class CoinGeckoService(PriceService):
    def __init__(self):
        self.base_url = settings.COINGECKO_BASE_URL
        self.api_key = settings.COINGECKO_API_KEY


    @with_retry
    def get_price(self, symbol: str) -> Optional[PriceResult]:
        symbol = symbol.upper()

        coingecko_ids = load_coingecko_ids()
        if symbol not in coingecko_ids:
            logger.warning("coingecko_symbol_not_found", symbol=symbol)
            return None

        coin_id = coingecko_ids[symbol]
        url = f"{self.base_url}/simple/price"

        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
        }

        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        with log_api_call(symbol, "coingecko"):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                price = data.get(coin_id, {}).get("usd")

                if price is None:
                    logger.error("coingecko_price_missing", symbol=symbol)
                    return None

                return PriceResult(
                    symbol=symbol,
                    price=Decimal(str(price)),
                    currency="USD",
                    provider="coingecko",
                    timestamp=datetime.utcnow(),
                )

            except requests.RequestException as e:
                logger.error("coingecko_request_exception", symbol=symbol, error=str(e))
                raise ProviderUnavailable(f"CoinGecko API failed: {e}")


    @with_retry
    def get_all_prices(self) -> Dict[str, PriceResult]:
        coingecko_ids = load_coingecko_ids()
        if not coingecko_ids:
            logger.warning("coingecko_no_ids_found")
            return {}

        url = f"{self.base_url}/simple/price"

        params = {
            "ids": ",".join(coingecko_ids.values()),
            "vs_currencies": "usd",
        }

        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        with log_api_call("ALL", "coingecko"):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                result = {}

                for symbol, coin_id in coingecko_ids.items():
                    if coin_id in data:
                        price = data[coin_id].get("usd")
                        if price is not None:
                            result[symbol] = PriceResult(
                                symbol=symbol,
                                price=Decimal(str(price)),
                                currency="USD",
                                provider="coingecko",
                                timestamp=datetime.utcnow(),
                            )

                logger.info("coingecko_all_prices_fetched", count=len(result))
                return result

            except requests.RequestException as e:
                logger.error("coingecko_all_prices_error", error=str(e))
                raise ProviderUnavailable(f"CoinGecko API failed: {e}")


    def get_history(self, symbol: str, days: int = 30) -> List[Dict]:
        symbol = symbol.upper()
        coingecko_ids = load_coingecko_ids()

        if symbol not in coingecko_ids:
            logger.warning("coingecko_symbol_not_found_history", symbol=symbol)
            return []

        coin_id = coingecko_ids[symbol]
        url = f"{self.base_url}/coins/{coin_id}/market_chart"

        params = {
            "vs_currency": "usd",
            "days": days,
        }

        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        with log_api_call(symbol, "coingecko_history"):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()

                # CoinGecko returns: [ [timestamp_ms, price], ... ]
                history = [
                    {"timestamp": ts, "price": float(price)}
                    for ts, price in data.get("prices", [])
                ]

                logger.info("coingecko_history_fetched", symbol=symbol, points=len(history))
                return history

            except requests.RequestException as e:
                logger.error("coingecko_history_error", symbol=symbol, error=str(e))
                raise ProviderUnavailable(f"CoinGecko history failed: {e}")
