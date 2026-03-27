from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.portfolio.urls", namespace="portfolio")),
    path("accounts/", include("django.contrib.auth.urls")),
]
