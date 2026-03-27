from fastapi import APIRouter, HTTPException, Depends
from typing import List

from api.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
    AllocationItem,
    SnapshotResponse,
)
from api.dependencies import get_current_user
from services.portfolio_service import get_portfolio_service
from repositories.portfolio_repository import PortfolioRepository
from django.contrib.auth.models import User

router = APIRouter()


@router.get("/", response_model=List[PortfolioResponse])
async def list_portfolios(user: User = Depends(get_current_user)):
    repo = PortfolioRepository()
    portfolios = repo.get_by_user(user.id)
    return [
        PortfolioResponse(
            id=p.id,
            name=p.name,
            total_invested=p.total_invested,
            current_value=p.current_value,
            total_pnl=p.total_pnl,
        )
        for p in portfolios
    ]


@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    data: PortfolioCreate, user: User = Depends(get_current_user)
):
    repo = PortfolioRepository()
    portfolio = repo.create(name=data.name, user_id=user.id)
    return PortfolioResponse(
        id=portfolio.id,
        name=portfolio.name,
        total_invested=portfolio.total_invested,
        current_value=portfolio.current_value,
        total_pnl=portfolio.total_pnl,
    )


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(portfolio_id: int, user: User = Depends(get_current_user)):
    service = get_portfolio_service()
    summary = service.get_portfolio_summary(portfolio_id)
    return PortfolioResponse(
        id=summary["id"],
        name=summary["name"],
        total_invested=summary["total_invested"],
        current_value=summary["current_value"],
        total_pnl=summary["total_pnl"],
    )


@router.get("/{portfolio_id}/allocation", response_model=List[AllocationItem])
async def get_allocation(portfolio_id: int, user: User = Depends(get_current_user)):
    service = get_portfolio_service()
    allocation = service.get_allocation(portfolio_id)
    return [AllocationItem(**item) for item in allocation]


@router.get("/{portfolio_id}/history", response_model=List[SnapshotResponse])
async def get_history(portfolio_id: int, user: User = Depends(get_current_user)):
    from apps.portfolio.models import PortfolioSnapshot

    snapshots = PortfolioSnapshot.objects.filter(portfolio_id=portfolio_id).order_by(
        "-date"
    )
    return [
        SnapshotResponse(
            id=s.id,
            date=str(s.date),
            value=s.value,
        )
        for s in snapshots
    ]
