from decimal import Decimal
from typing import Optional

from django.db.models import QuerySet

from apps.wallet.models import Holding


class HoldingRepository:
    def get_by_id(self, holding_id: int) -> Optional[Holding]:
        try:
            return Holding.objects.select_related("asset", "portfolio").get(
                id=holding_id
            )
        except Holding.DoesNotExist:
            return None

    def get_by_portfolio(self, portfolio_id: int) -> QuerySet[Holding]:
        return Holding.objects.filter(portfolio_id=portfolio_id).select_related("asset")

    def create(
        self,
        portfolio_id: int,
        asset_id: int,
        quantity: Decimal,
        avg_buy_price: Decimal,
    ) -> Holding:
        from apps.portfolio.models import Portfolio
        from apps.wallet.models import Asset

        portfolio = Portfolio.objects.get(id=portfolio_id)
        asset = Asset.objects.get(id=asset_id)

        return Holding.objects.create(
            portfolio=portfolio,
            asset=asset,
            quantity=quantity,
            avg_buy_price=avg_buy_price,
        )

    def update(
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

    def delete(self, holding_id: int) -> None:
        holding = Holding.objects.get(id=holding_id)
        holding.delete()
