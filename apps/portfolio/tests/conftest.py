import pytest
from decimal import Decimal


@pytest.fixture
def user():
    from django.contrib.auth.models import User

    return User(username="testuser", email="test@example.com")


@pytest.fixture
def portfolio(user):
    from apps.portfolio.models import Portfolio

    return Portfolio(name="Test Portfolio", user=user)
