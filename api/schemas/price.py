from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PriceResponse(BaseModel):
    symbol: str
    price: Decimal
    currency: str
    provider: str
    timestamp: datetime


class PriceListResponse(BaseModel):
    prices: dict[str, PriceResponse]
