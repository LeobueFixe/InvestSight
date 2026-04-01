from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.wallet.models import Wallet
from services.wallet_service import WalletService


@login_required
def wallet_view(request):
    wallet = Wallet.objects.filter(user=request.user).first()
    return render(request, "wallet/wallet.html", {"wallet": wallet})


@login_required
def wallet_create(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password or len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("wallet:create")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("wallet:create")

        existing = Wallet.objects.filter(user=request.user).first()
        if existing:
            messages.error(request, "Wallet already exists.")
            return redirect("wallet:wallet")

        service = WalletService()
        wallet, seed_phrase = service.create_wallet(request.user, password)
        request.session["pending_seed_phrase"] = seed_phrase
        return redirect("wallet:show_seed")

    return render(request, "wallet/create.html")


@login_required
def wallet_show_seed(request):
    seed_phrase = request.session.pop("pending_seed_phrase", None)
    if not seed_phrase:
        messages.error(request, "No seed phrase to display.")
        return redirect("wallet:wallet")
    return render(request, "wallet/show_seed.html", {"seed_phrase": seed_phrase})


@login_required
def wallet_restore(request):
    if request.method == "POST":
        seed_phrase = request.POST.get("seed_phrase", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not seed_phrase:
            messages.error(request, "Please enter a seed phrase.")
            return redirect("wallet:restore")

        if not password or len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("wallet:restore")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("wallet:restore")

        service = WalletService()
        try:
            wallet = service.restore_wallet(request.user, seed_phrase, password)
            messages.success(request, "Wallet restored successfully!")
            return redirect("wallet:wallet")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("wallet:restore")

    return render(request, "wallet/restore.html")
