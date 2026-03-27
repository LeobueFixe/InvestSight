from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.portfolio.urls", namespace="portfolio")),
    path("wallet/", include("apps.wallet.urls", namespace="wallet")),
    path("accounts/", include("django.contrib.auth.urls")),
]
