from datetime import date
from decimal import Decimal
from typing import Optional

from apps.portfolio.models import Portfolio, PortfolioSnapshot


class PortfolioService:
    def get_portfolio_summary(self, portfolio_id: int) -> dict:
        portfolio = Portfolio.objects.prefetch_related("holdings__asset").get(
            id=portfolio_id
        )
        return {
            "id": portfolio.id,
            "name": portfolio.name,
            "total_invested": portfolio.total_invested,
            "current_value": portfolio.current_value,
            "total_pnl": portfolio.total_pnl,
            "allocation": portfolio.get_allocation(),
        }

    def get_allocation(self, portfolio_id: int) -> list[dict]:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        return portfolio.get_allocation()

    def capture_snapshot(self, portfolio_id: int) -> PortfolioSnapshot:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        current_value = portfolio.current_value

        if current_value is None:
            current_value = Decimal("0")

        snapshot, created = PortfolioSnapshot.objects.update_or_create(
            portfolio=portfolio, date=date.today(), defaults={"value": current_value}
        )
        return snapshot


_portfolio_service = None


def get_portfolio_service() -> PortfolioService:
    global _portfolio_service
    if _portfolio_service is None:
        _portfolio_service = PortfolioService()
    return _portfolio_service
