from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path("", views.wallet_view, name="wallet"),
    path("create/", views.wallet_create, name="create"),
    path("show-seed/", views.wallet_show_seed, name="show_seed"),
    path("restore/", views.wallet_restore, name="restore"),
]
