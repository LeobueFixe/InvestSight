from decimal import Decimal
from typing import Optional

from apps.wallet.models import Holding, Asset


class HoldingService:
    def create_holding(
        self,
        portfolio_id: int,
        asset_id: int,
        quantity: Decimal,
        avg_buy_price: Decimal,
    ) -> Holding:
        from apps.portfolio.models import Portfolio

        portfolio = Portfolio.objects.get(id=portfolio_id)
        asset = Asset.objects.get(id=asset_id)

        holding = Holding.objects.create(
            portfolio=portfolio,
            asset=asset,
            quantity=quantity,
            avg_buy_price=avg_buy_price,
        )
        return holding

    def get_holding_detail(self, holding_id: int) -> dict:
        holding = Holding.objects.select_related("asset", "portfolio").get(
            id=holding_id
        )
        return {
            "id": holding.id,
            "asset": holding.asset.symbol,
            "asset_name": holding.asset.name,
            "quantity": holding.quantity,
            "avg_buy_price": holding.avg_buy_price,
            "total_cost": holding.total_cost,
            "current_value": holding.current_value,
            "profit_loss": holding.profit_loss,
            "pnl_pct": holding.pnl_pct,
        }

    def update_holding(
        self,
        holding_id: int,
        quantity: Optional[Decimal] = None,
        avg_buy_price: Optional[Decimal] = None,
    ) -> Holding:
        holding = Holding.objects.get(id=holding_id)
        if quantity is not None:
            holding.quantity = quantity
        if avg_buy_price is not None:
            holding.avg_buy_price = avg_buy_price
        holding.save()
        return holding

    def delete_holding(self, holding_id: int) -> None:
        holding = Holding.objects.get(id=holding_id)
        holding.delete()
