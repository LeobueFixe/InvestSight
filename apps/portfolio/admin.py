from django.contrib import admin
from .models import Portfolio, PortfolioSnapshot, Alert


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at"]
    search_fields = ["name", "user__username"]


@admin.register(PortfolioSnapshot)
class PortfolioSnapshotAdmin(admin.ModelAdmin):
    list_display = ["portfolio", "date", "value"]
    list_filter = ["date"]
    readonly_fields = ["created_at"]


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = [
        "portfolio",
        "asset",
        "target_price",
        "direction",
        "active",
        "triggered",
    ]
    list_filter = ["active", "triggered", "direction"]
