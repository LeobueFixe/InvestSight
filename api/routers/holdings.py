from fastapi import APIRouter, HTTPException, Depends
from typing import List

from api.schemas.holding import HoldingCreate, HoldingUpdate, HoldingResponse
from api.dependencies import get_current_user
from services.holding_service import HoldingService
from django.contrib.auth.models import User
from apps.wallet.models import Holding

router = APIRouter()


@router.get("/", response_model=List[HoldingResponse])
async def list_holdings(user: User = Depends(get_current_user)):
    holdings = Holding.objects.filter(portfolio__user=user).select_related(
        "asset", "portfolio"
    )
    return [
        HoldingResponse(
            id=h.id,
            asset_symbol=h.asset.symbol,
            asset_name=h.asset.name,
            quantity=h.quantity,
            avg_buy_price=h.avg_buy_price,
            total_cost=h.total_cost,
            current_value=h.current_value,
            profit_loss=h.profit_loss,
            pnl_pct=h.pnl_pct,
        )
        for h in holdings
    ]


@router.post("/", response_model=HoldingResponse)
async def create_holding(data: HoldingCreate, user: User = Depends(get_current_user)):
    service = HoldingService()
    holding = service.create_holding(
        portfolio_id=data.portfolio_id,
        asset_id=data.asset_id,
        quantity=data.quantity,
        avg_buy_price=data.avg_buy_price,
    )
    return HoldingResponse(
        id=holding.id,
        asset_symbol=holding.asset.symbol,
        asset_name=holding.asset.name,
        quantity=holding.quantity,
        avg_buy_price=holding.avg_buy_price,
        total_cost=holding.total_cost,
        current_value=holding.current_value,
        profit_loss=holding.profit_loss,
        pnl_pct=holding.pnl_pct,
    )


@router.get("/{holding_id}", response_model=HoldingResponse)
async def get_holding(holding_id: int, user: User = Depends(get_current_user)):
    service = HoldingService()
    detail = service.get_holding_detail(holding_id)
    return HoldingResponse(
        id=holding_id,
        asset_symbol=detail["asset"],
        asset_name=detail["asset_name"],
        quantity=detail["quantity"],
        avg_buy_price=detail["avg_buy_price"],
        total_cost=detail["total_cost"],
        current_value=detail["current_value"],
        profit_loss=detail["profit_loss"],
        pnl_pct=detail["pnl_pct"],
    )


@router.put("/{holding_id}", response_model=HoldingResponse)
async def update_holding(
    holding_id: int, data: HoldingUpdate, user: User = Depends(get_current_user)
):
    service = HoldingService()
    holding = service.update_holding(holding_id, data.quantity, data.avg_buy_price)
    return HoldingResponse(
        id=holding.id,
        asset_symbol=holding.asset.symbol,
        asset_name=holding.asset.name,
        quantity=holding.quantity,
        avg_buy_price=holding.avg_buy_price,
        total_cost=holding.total_cost,
        current_value=holding.current_value,
        profit_loss=holding.profit_loss,
        pnl_pct=holding.pnl_pct,
    )


@router.delete("/{holding_id}")
async def delete_holding(holding_id: int, user: User = Depends(get_current_user)):
    service = HoldingService()
    service.delete_holding(holding_id)
    return {"status": "deleted"}
