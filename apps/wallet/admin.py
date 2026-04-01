from django.contrib import admin
from .models import Asset, Holding, Wallet


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["symbol", "name", "asset_type", "created_at"]
    search_fields = ["symbol", "name"]
    list_filter = ["asset_type"]


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ["asset", "portfolio", "quantity", "avg_buy_price", "updated_at"]
    list_filter = ["asset__asset_type"]
    search_fields = ["asset__symbol"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    search_fields = ["user__username"]
