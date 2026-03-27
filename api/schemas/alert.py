from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    portfolio_id: int
    asset_id: int
    target_price: Decimal = Field(max_digits=20, decimal_places=8)
    direction: str = Field(pattern="^(above|below)$")


class AlertResponse(BaseModel):
    id: int
    asset_symbol: str
    target_price: Decimal
    direction: str
    active: bool
    triggered: bool
    triggered_at: datetime | None
