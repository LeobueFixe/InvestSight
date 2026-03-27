from decimal import Decimal
from pydantic import BaseModel, Field


class HoldingCreate(BaseModel):
    portfolio_id: int
    asset_id: int
    quantity: Decimal = Field(max_digits=20, decimal_places=8)
    avg_buy_price: Decimal = Field(max_digits=20, decimal_places=8)


class HoldingUpdate(BaseModel):
    quantity: Decimal = Field(max_digits=20, decimal_places=8)
    avg_buy_price: Decimal = Field(max_digits=20, decimal_places=8)


class HoldingResponse(BaseModel):
    id: int
    asset_symbol: str
    asset_name: str
    quantity: Decimal
    avg_buy_price: Decimal
    total_cost: Decimal
    current_value: Decimal | None
    profit_loss: Decimal | None
    pnl_pct: Decimal | None
