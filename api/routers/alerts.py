from fastapi import APIRouter, Depends
from typing import List

from api.schemas.alert import AlertCreate, AlertResponse
from api.dependencies import get_current_user
from repositories.alert_repository import AlertRepository
from django.contrib.auth.models import User

router = APIRouter()


@router.get("/{portfolio_id}/alerts", response_model=List[AlertResponse])
async def list_alerts(portfolio_id: int, user: User = Depends(get_current_user)):
    repo = AlertRepository()
    alerts = repo.get_by_portfolio(portfolio_id)
    return [
        AlertResponse(
            id=a.id,
            asset_symbol=a.asset.symbol,
            target_price=a.target_price,
            direction=a.direction,
            active=a.active,
            triggered=a.triggered,
            triggered_at=a.triggered_at,
        )
        for a in alerts
    ]


@router.post("/{portfolio_id}/alerts", response_model=AlertResponse)
async def create_alert(
    portfolio_id: int, data: AlertCreate, user: User = Depends(get_current_user)
):
    repo = AlertRepository()
    alert = repo.create(
        portfolio_id=data.portfolio_id,
        asset_id=data.asset_id,
        target_price=data.target_price,
        direction=data.direction,
    )
    return AlertResponse(
        id=alert.id,
        asset_symbol=alert.asset.symbol,
        target_price=alert.target_price,
        direction=alert.direction,
        active=alert.active,
        triggered=alert.triggered,
        triggered_at=alert.triggered_at,
    )
