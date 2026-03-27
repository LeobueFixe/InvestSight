from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from apps.portfolio.models import Portfolio
from apps.wallet.models import Holding, SeedPhrase


# Register of new users
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Portfolio.objects.create(name="My Portfolio", user=user)
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# Show the dashboard of the user when he is logged in
@login_required
def index(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, "portfolio/dashboard.html", {"portfolios": portfolios})


# Shows a specific portfolio of the user.It needs to be authenticated!
@login_required
def detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    holdings = portfolio.holdings.select_related("asset")
    allocation = portfolio.get_allocation()
    return render(
        request,
        "portfolio/detail.html",
        {
            "portfolio": portfolio,
            "holdings": holdings,
            "allocation": allocation,
        },
    )


# Shows the user's wallet!
@login_required
def wallet(request):
    holdings = Holding.objects.filter(portfolio__user=request.user).select_related(
        "asset", "portfolio"
    )
    seed_phrase = getattr(request.user, "seed_phrase", None)
    if not seed_phrase:
        seed_phrase = SeedPhrase.objects.create(user=request.user)
    return render(
        request,
        "portfolio/wallet.html",
        {"holdings": holdings, "seed_phrase": seed_phrase},
    )
