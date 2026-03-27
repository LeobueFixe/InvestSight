from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("wallet/", views.wallet, name="wallet"),
    path("", views.index, name="index"),
    path("<int:portfolio_id>/", views.detail, name="detail"),
]
