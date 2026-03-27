from decimal import Decimal
from pydantic import BaseModel, Field


class PortfolioCreate(BaseModel):
    name: str = Field(max_length=200)


class PortfolioUpdate(BaseModel):
    name: str = Field(max_length=200)


class PortfolioResponse(BaseModel):
    id: int
    name: str
    total_invested: Decimal
    current_value: Decimal | None
    total_pnl: Decimal | None


class AllocationItem(BaseModel):
    asset: str
    value: Decimal
    pct_of_portfolio: float


class SnapshotResponse(BaseModel):
    id: int
    date: str
    value: Decimal
