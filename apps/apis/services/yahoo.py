import yfinance
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, List
from pathlib import Path
import json

from apps.apis.exceptions import ProviderUnavailable
from apps.apis.services.base import PriceResult, PriceService
from apps.apis.services.retry import with_retry
from apps.apis.services.logging import get_logger, log_api_call
from apps.apis.settings import settings

DATA_FILE = Path("apps/apis/data/prices.json")
logger = get_logger("yahoo")
YAHOO_FINANCE_ENABLED = settings.YAHOO_FINANCE_ENABLED



def load_yahoo_ids() -> Dict[str, str]:
    """
    Loads Yahoo Finance symbol → ticker mapping from data/prices.json.
    """
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {}

    return data.get("yahoo_ids", {})



class YahooFinanceService(PriceService):
    """
    Price provider using yfinance.
    Supports:
      - current price
      - all prices
      - historical data
    """


    @with_retry
    def get_price(self, symbol: str) -> Optional[PriceResult]:
        if not YAHOO_FINANCE_ENABLED:
            logger.info("yahoo_disabled", symbol=symbol)
            return None

        symbol = symbol.upper()
        yahoo_ids = load_yahoo_ids()

        if symbol not in yahoo_ids:
            logger.warning("yahoo_symbol_not_found", symbol=symbol)
            return None

        ticker_symbol = yahoo_ids[symbol]

        with log_api_call(symbol, "yahoo"):
            try:
                ticker = yfinance.Ticker(ticker_symbol)
                info = ticker.info

                price = info.get("currentPrice") or info.get("regularMarketPreviousClose")
                if price is None:
                    logger.error("yahoo_price_missing", symbol=symbol)
                    return None

                return PriceResult(
                    symbol=symbol,
                    price=Decimal(str(price)),
                    currency="USD",
                    provider="yahoo",
                    timestamp=datetime.utcnow(),
                )

            except Exception as e:
                logger.error("yahoo_request_exception", symbol=symbol, error=str(e))
                raise ProviderUnavailable(f"Yahoo Finance API failed: {e}")


    @with_retry
    def get_all_prices(self) -> Dict[str, PriceResult]:
        if not YAHOO_FINANCE_ENABLED:
            logger.info("yahoo_disabled_all_prices")
            return {}

        yahoo_ids = load_yahoo_ids()
        result = {}

        with log_api_call("ALL", "yahoo"):
            for symbol in yahoo_ids:
                try:
                    price_result = self.get_price(symbol)
                    if price_result:
                        result[symbol] = price_result
                except Exception as e:
                    logger.error("yahoo_symbol_failed", symbol=symbol, error=str(e))

            logger.info("yahoo_all_prices_fetched", count=len(result))
            return result


    def get_history(self, symbol: str, days: int = 30) -> List[Dict]:
        """
        Returns historical daily close prices for the last N days.
        """
        if not YAHOO_FINANCE_ENABLED:
            logger.info("yahoo_disabled_history", symbol=symbol)
            return []

        symbol = symbol.upper()
        yahoo_ids = load_yahoo_ids()

        if symbol not in yahoo_ids:
            logger.warning("yahoo_symbol_not_found_history", symbol=symbol)
            return []

        ticker_symbol = yahoo_ids[symbol]

        with log_api_call(symbol, "yahoo_history"):
            try:
                ticker = yfinance.Ticker(ticker_symbol)
                df = ticker.history(period=f"{days}d")

                history = [
                    {
                        "timestamp": int(row.name.timestamp() * 1000),
                        "price": float(row["Close"]),
                    }
                    for _, row in df.iterrows()
                ]

                logger.info("yahoo_history_fetched", symbol=symbol, points=len(history))
                return history

            except Exception as e:
                logger.error("yahoo_history_error", symbol=symbol, error=str(e))
                raise ProviderUnavailable(f"Yahoo Finance history failed: {e}")
