from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from apps.portfolio.models import Portfolio, PortfolioSnapshot


class Command(BaseCommand):
    help = "Capture daily snapshots for all portfolios"

    def handle(self, *args, **options):
        portfolios = Portfolio.objects.all()
        count = 0

        for portfolio in portfolios:
            current_value = portfolio.current_value
            if current_value is None:
                current_value = Decimal("0")

            snapshot, created = PortfolioSnapshot.objects.update_or_create(
                portfolio=portfolio,
                date=date.today(),
                defaults={"value": current_value},
            )

            status = "Created" if created else "Updated"
            self.stdout.write(
                f"{status} snapshot for {portfolio.name}: ${current_value}"
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Captured {count} snapshots"))
