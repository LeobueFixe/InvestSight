# CLAUDE.md -- InvestSight

This file is the authoritative instruction set for Claude Code when working on this project.
Read it in full before taking any action. Follow every constraint exactly as written.
When in doubt, ask rather than assume.

---

## 1. Project Overview

**InvestSight** is a crypto and stock portfolio tracker built with Django and FastAPI.
It is a capstone project for the Backend I module. Each student in the group builds their
own domain independently, but all domains integrate into a single cohesive application.
The goal is to demonstrate sound architectural thinking, intentional tool selection, and
professional-grade project hygiene. Think of this as a portfolio piece.

The project tracks holdings across crypto (BTC, ETH) and stock (AAPL, TSLA) assets,
fetches live prices from CoinGecko and Yahoo Finance, computes profit/loss at both
the holding and portfolio level, and provides performance history and allocation breakdowns.

**Team and ownership:**

| Member  | Domain    | Responsibility                                                    |
|---------|-----------|-------------------------------------------------------------------|
| Leo     | APIs      | Price fetching, caching, error handling, rate limits, logging     |
| Paulo   | Wallet    | Asset and Holding models, P&L calculations, decimal precision     |
| Rodrigo | Portfolio | Portfolio aggregations, alerts, snapshots, allocation breakdowns  |
| Team    | Shared    | Service layer, repository pattern, settings, tests, documentation |

---

## 2. Technology Stack

| Layer              | Technology                | Notes                                                        |
|--------------------|---------------------------|--------------------------------------------------------------|
| Web framework      | Django 5.x                | ORM, admin, models, templates, session management            |
| API framework      | FastAPI                   | All REST API endpoints. Django handles no API views.         |
| Language           | Python 3.12+              | Type hints encouraged throughout                             |
| Database           | SQLite                    | Default Django SQLite backend. No PostgreSQL.                |
| Cache              | Django built-in cache     | `django.core.cache` with `LocMemCache` backend               |
| Sessions           | Django DB sessions        | `django.contrib.sessions.backends.db`                        |
| HTTP client        | `requests`                | For CoinGecko and Yahoo Finance API calls                    |
| Finance data       | `yfinance`                | For AAPL/TSLA stock price fetching                           |
| Retry logic        | `tenacity`                | Exponential backoff with jitter for rate-limited APIs        |
| Structured logging | `structlog`               | JSON-formatted logs for all API calls                        |
| Environment config | `django-environ`          | All config loaded from `.env`                                |
| Testing            | `pytest` + `pytest-django`| With `pytest-mock`, `responses` or `pytest-httpretty`        |
| Frontend           | Django Templates + HTMX   | Minimal UI. No React, no Vue, no SPA.                       |
| Containerisation   | None                      | Run locally with `manage.py` and `uvicorn`                   |

**Explicitly excluded technologies (do NOT install or use):**

- Redis or `django-redis`
- Celery or any task queue
- JWT or token-based auth (`djangorestframework-simplejwt`, `PyJWT`, etc.)
- Django REST Framework (all API endpoints use FastAPI)
- PostgreSQL or any database other than SQLite
- Nginx, Gunicorn, or any reverse proxy

---

## 3. Repository Structure

Create exactly this layout. Do not add extra top-level directories without instruction.

```
investsight/
├── CLAUDE.md
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
├── config/                        # Django project package
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py               # Stubbed, not wired up
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── apis/                      # Leo's domain: price fetching services
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── config.py              # Centralised API keys, base URLs, TTLs (L9)
│   │   ├── exceptions.py          # PriceAPIError, ProviderUnavailable (L6)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # PriceService ABC + PriceResult dataclass (L1)
│   │   │   ├── mock.py            # Mock price provider (L1)
│   │   │   ├── coingecko.py       # CoinGecko integration (L2)
│   │   │   ├── yahoo.py           # Yahoo Finance integration (L3)
│   │   │   ├── unified.py         # Unified get_price(symbol) router (L4)
│   │   │   ├── cache.py           # Cache wrapper around unified service (L5)
│   │   │   ├── retry.py           # Rate limit handling + backoff (L7)
│   │   │   └── logging.py         # Structured JSON logging (L8)
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py        # Shared fixtures
│   │       ├── fixtures/          # Recorded JSON payloads (L11)
│   │       │   ├── coingecko_btc.json
│   │       │   ├── coingecko_eth.json
│   │       │   ├── yahoo_aapl.json
│   │       │   └── yahoo_tsla.json
│   │       ├── test_mock.py
│   │       ├── test_coingecko.py
│   │       ├── test_yahoo.py
│   │       ├── test_unified.py
│   │       ├── test_cache.py
│   │       ├── test_error_handling.py
│   │       ├── test_retry.py
│   │       ├── test_logging.py
│   │       └── test_config.py
│   ├── wallet/                    # Paulo's domain: holdings and calculations
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # Asset, Holding models
│   │   ├── admin.py
│   │   ├── migrations/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── test_asset.py
│   │       ├── test_holding.py
│   │       ├── test_pnl.py
│   │       ├── test_currency.py
│   │       └── test_decimal.py
│   └── portfolio/                 # Rodrigo's domain: aggregations and analytics
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py              # Portfolio, PortfolioSnapshot, Alert models
│       ├── admin.py
│       ├── migrations/
│       └── tests/
│           ├── __init__.py
│           ├── conftest.py
│           ├── test_totals.py
│           ├── test_pnl.py
│           ├── test_snapshots.py
│           ├── test_alerts.py
│           └── test_allocation.py
├── services/                      # Shared service layer (A1)
│   ├── __init__.py
│   ├── price_service.py
│   ├── holding_service.py
│   └── portfolio_service.py
├── repositories/                  # Shared repository pattern (A2)
│   ├── __init__.py
│   ├── holding_repository.py
│   ├── portfolio_repository.py
│   └── alert_repository.py
├── api/                           # FastAPI application
│   ├── __init__.py
│   ├── main.py                    # FastAPI app instance
│   ├── dependencies.py            # Shared dependencies (DB session, services)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── price.py               # Pydantic models for price responses
│   │   ├── holding.py             # Pydantic models for holding responses
│   │   ├── portfolio.py           # Pydantic models for portfolio responses
│   │   └── alert.py               # Pydantic models for alert responses
│   └── routers/
│       ├── __init__.py
│       ├── prices.py              # /api/prices/ endpoints
│       ├── holdings.py            # /api/holdings/ endpoints
│       ├── portfolios.py          # /api/portfolios/ endpoints
│       └── alerts.py              # /api/alerts/ endpoints
├── templates/
│   ├── base.html
│   ├── partials/
│   │   └── navbar.html
│   ├── portfolio/
│   │   ├── dashboard.html
│   │   └── detail.html
│   └── holdings/
│       └── list.html
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
├── docs/                          # Architecture documentation (DOC3)
│   ├── architecture.md
│   ├── data_flow.md
│   └── diagrams/
└── tests/                         # Integration tests (T4)
    ├── __init__.py
    └── test_integration.py
```

---

## 4. Django Apps

Each app lives under `apps/`. Register them in `INSTALLED_APPS` as `apps.apis`, `apps.wallet`,
`apps.portfolio`. Each app must have its own `apps.py`, `models.py` (where applicable),
`admin.py` (where applicable), and a `tests/` package.

**Important:** Django apps handle models, ORM, admin, and migrations only. All API endpoints
are served by FastAPI in the `api/` package. Django views are limited to template rendering
for the minimal HTMX frontend.

### 4.1 apps.apis (Owner: Leo)

**Purpose:** Price fetching services for crypto and stock assets.

**This app has no Django models.** It is a pure service layer that wraps external API calls
(CoinGecko, Yahoo Finance) behind a unified interface, with caching, error handling,
rate limiting, retry logic, and structured logging.

**Key components:**

- `config.py` -- Centralises all API keys, base URLs, TTLs, retry counts. Loaded from `.env`
  via `django-environ`. No hardcoded strings outside this module. Provides `.env.example`
  template. (Task L9)
- `exceptions.py` -- Custom exceptions: `PriceAPIError`, `ProviderUnavailable`. (Task L6)
- `services/base.py` -- `PriceService` abstract base class defining the interface.
  `PriceResult` dataclass with fields: `symbol`, `price` (Decimal), `currency` (str),
  `provider` (str), `timestamp` (datetime). (Task L1)
- `services/mock.py` -- Static dict returning hardcoded prices for BTC, ETH, AAPL, TSLA.
  Implements `PriceService` ABC. Entry point and fallback provider. (Task L1)
- `services/coingecko.py` -- HTTP call to CoinGecko `/simple/price` endpoint. Parses JSON,
  extracts USD price for BTC and ETH. Uses `requests` library. Base URL from env var
  `COINGECKO_BASE_URL`. (Task L2)
- `services/yahoo.py` -- Uses `yfinance` library to fetch AAPL/TSLA stock prices. Symbol
  validation required. Handles `Ticker.info` access. (Task L3)
- `services/unified.py` -- Single `get_price(symbol)` interface that routes to CoinGecko
  or Yahoo Finance based on asset type. Uses registry pattern: `{symbol: provider}`. Returns
  `PriceResult` dataclass. Normalised output using Decimal. (Task L4)
- `services/cache.py` -- Wraps API responses in Django cache backend (`django.core.cache`).
  TTL configurable per asset type. Key pattern: `price:{symbol}:{date}`. (Task L5)
- `services/retry.py` -- Detects 429 responses, implements exponential backoff with jitter,
  max 3 retries. Uses `tenacity` library. Logs each retry attempt. (Task L7)
- `services/logging.py` -- Structured JSON logs for every API call: `symbol`, `provider`,
  `latency_ms`, `status`, `cache_hit`. Uses Python `logging` + `structlog`. Log level
  configurable via env var. Includes `correlation_id`. (Task L8)

### 4.2 apps.wallet (Owner: Paulo)

**Purpose:** Asset and Holding models with all financial calculations.

**Models:** `Asset`, `Holding` (see Section 5).

**Key behaviours:**

- `Asset.current_price` -- Model property that calls the unified price service and returns
  a live Decimal price. Handles None gracefully. (Task P1)
- `Holding.total_cost` -- Property: `quantity * avg_buy_price` using Decimal arithmetic.
  Uses `Decimal(str(value))` for any inputs originating from floats. (Task P2)
- `Holding.current_value` -- Property: `quantity * asset.current_price`. Leverages cache
  from L5. Considers a staleness flag. (Task P3)
- `Holding.profit_loss` -- Property: `current_value - total_cost`. Handles gain, loss,
  and breakeven. Returns signed Decimal. Consider unrealised vs realised flag. (Task P4)
- `Holding.pnl_pct` -- Property: `(profit_loss / total_cost) * 100`. Guards against
  division by zero when `total_cost == 0`. Returns `Optional[Decimal]`. Document
  None semantics. (Task P5)
- Currency normalisation: all monetary values convert to base currency (USD) before storage
  and calculation. FX rates can be hardcoded initially with a TODO for live FX. (Task P7)
- Decimal precision: all float fields replaced with
  `DecimalField(max_digits=20, decimal_places=8)` across models. No float arithmetic
  anywhere in the codebase. (Task P8)

### 4.3 apps.portfolio (Owner: Rodrigo)

**Purpose:** Portfolio-level aggregations, performance history, alerts, and allocation.

**Models:** `Portfolio`, `PortfolioSnapshot`, `Alert` (see Section 5).

**Key behaviours:**

- `Portfolio.total_invested` -- Aggregates `Holding.total_cost` across all holdings via
  ORM query using `aggregate(Sum('total_cost'))`. Cache result if expensive. (Task R1)
- `Portfolio.current_value` -- Aggregates `Holding.current_value`. Uses batch price lookups
  to avoid N+1. Uses `select_related`. (Task R2)
- `Portfolio.total_pnl` -- `current_value - total_invested`. Exposes both absolute and
  percentage variants. Reuses P4/P5 logic at portfolio level. (Task R3)
- `PortfolioRepository.get_holdings(portfolio_id)` -- Returns queryset filtered by portfolio,
  with `select_related` and `prefetch_related`. No N+1 queries. Part of Repository
  pattern (A2). Returns typed QuerySet. (Task R4)
- `AlertRepository.get_active(portfolio_id)` -- Returns only alerts where `active=True`
  and not yet triggered. Index on `(portfolio_id, active)`. Consider soft-delete
  pattern. (Task R5)
- Performance history: `PortfolioSnapshot` model stores daily `current_value`. A Django
  management command (not Celery) triggers daily snapshot capture. Model fields:
  `portfolio` (FK), `date` (DateField), `value` (DecimalField). DB index on `date`.
  (Task R7)
- Allocation breakdown: returns list of `{asset, value, pct_of_portfolio}` dicts. Sorted
  by allocation descending. Percentages sum to 100%. Rounded to 2 decimal places. JSON
  serialisable. (Task R8)

---

## 5. Data Models

Define wallet-related models in `apps/wallet/models.py`.
Define portfolio-related models in `apps/portfolio/models.py`.

### 5.1 Wallet Models (apps/wallet/models.py)

#### AssetType (TextChoices)

```python
class AssetType(models.TextChoices):
    CRYPTO = 'crypto', 'Cryptocurrency'
    STOCK  = 'stock',  'Stock'
```

#### Asset

```
id              -- AutoField PK
symbol          -- CharField(max_length=20, unique=True)      # e.g. "BTC", "AAPL"
name            -- CharField(max_length=200)                   # e.g. "Bitcoin", "Apple Inc."
asset_type      -- CharField(max_length=20, choices=AssetType.choices)
created_at      -- DateTimeField(auto_now_add=True)
```

Rules:
- `symbol` is always stored uppercase. Enforce in `save()` with `self.symbol = self.symbol.upper()`.
- `current_price` is a property (not a field). It calls `PriceService.get_price(self.symbol)`
  and returns a Decimal or None.
- `__str__` returns `"{symbol} ({name})"`, e.g. `"BTC (Bitcoin)"`.

#### Holding

```
id              -- AutoField PK
portfolio       -- FK('portfolio.Portfolio', on_delete=CASCADE, related_name='holdings')
asset           -- FK(Asset, on_delete=PROTECT, related_name='holdings')
quantity        -- DecimalField(max_digits=20, decimal_places=8)
avg_buy_price   -- DecimalField(max_digits=20, decimal_places=8)  # average cost basis in USD
created_at      -- DateTimeField(auto_now_add=True)
updated_at      -- DateTimeField(auto_now=True)
```

Rules:
- All monetary and quantity fields use `DecimalField(max_digits=20, decimal_places=8)`.
  Never use `FloatField` for any financial value.
- `total_cost`, `current_value`, `profit_loss`, `pnl_pct` are all properties, not fields.
- Use `Decimal(str(value))` when converting any float input to Decimal.
- A holding with `quantity == 0` is valid (fully sold position) but should be excluded
  from active aggregations.

### 5.2 Portfolio Models (apps/portfolio/models.py)

#### Portfolio

```
id              -- AutoField PK
name            -- CharField(max_length=200)
user            -- FK(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='portfolios')
created_at      -- DateTimeField(auto_now_add=True)
updated_at      -- DateTimeField(auto_now=True)
```

Rules:
- `total_invested`, `current_value`, `total_pnl` are properties or methods, not fields.
- Uses Django's built-in `User` model. No custom user model.
- `__str__` returns `"{name} ({user.username})"`.

#### PortfolioSnapshot

```
id              -- AutoField PK
portfolio       -- FK(Portfolio, on_delete=CASCADE, related_name='snapshots')
date            -- DateField()
value           -- DecimalField(max_digits=20, decimal_places=2)
created_at      -- DateTimeField(auto_now_add=True)
```

Rules:
- Unique together on `(portfolio, date)` -- one snapshot per portfolio per day.
- Add a DB index on `date` in `Meta.indexes`.
- Snapshots are created by a Django management command (`python manage.py capture_snapshots`),
  NOT by Celery. This command can be scheduled via cron or run manually.

#### Alert

```
id              -- AutoField PK
portfolio       -- FK(Portfolio, on_delete=CASCADE, related_name='alerts')
asset           -- FK('wallet.Asset', on_delete=CASCADE)
target_price    -- DecimalField(max_digits=20, decimal_places=8)
direction       -- CharField(max_length=10, choices=[('above', 'Above'), ('below', 'Below')])
active          -- BooleanField(default=True)
triggered       -- BooleanField(default=False)
triggered_at    -- DateTimeField(null=True, blank=True)
created_at      -- DateTimeField(auto_now_add=True)
```

Rules:
- An alert is "active" when `active=True` and `triggered=False`.
- Index on `(portfolio, active)` for efficient querying.
- Consider soft-delete pattern: never hard-delete alerts.

---

## 6. Session and Cache Architecture

### Session Configuration

Use Django's database-backed sessions. No Redis.

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 14 days
SESSION_SAVE_EVERY_REQUEST = False
```

### Cache Configuration

Use Django's local memory cache. No Redis, no Memcached.

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'investsight-cache',
        'TIMEOUT': 300,  # 5 minutes default TTL
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    }
}
```

The price service (L5) uses this cache backend with key pattern `price:{symbol}:{date}`.
TTL is configurable per asset type via the API config module (L9).

---

## 7. Django + FastAPI Integration

Django handles: ORM, models, migrations, admin, templates, sessions, management commands.
FastAPI handles: all REST API endpoints.

### Integration approach

FastAPI runs alongside Django using `uvicorn`. Django's WSGI app is mounted inside
FastAPI for template rendering and admin access, or they run as separate processes
on different ports.

**Recommended approach:** Run both on the same process using `django-ninja` patterns
but with pure FastAPI. In `api/main.py`:

```python
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from fastapi import FastAPI
from api.routers import prices, holdings, portfolios, alerts

app = FastAPI(
    title="InvestSight API",
    description="Crypto and stock portfolio tracker",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(prices.router, prefix="/api/prices", tags=["Prices"])
app.include_router(holdings.router, prefix="/api/holdings", tags=["Holdings"])
app.include_router(portfolios.router, prefix="/api/portfolios", tags=["Portfolios"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
```

### Running the project

```bash
# Terminal 1: Django dev server (admin + templates)
python manage.py runserver 8000

# Terminal 2: FastAPI dev server (API endpoints)
uvicorn api.main:app --reload --port 8001
```

### Authentication for API endpoints

Use Django sessions for authentication. FastAPI endpoints read the Django session cookie
to identify the logged-in user. No JWT. No token-based auth.

Create a FastAPI dependency in `api/dependencies.py` that reads the session from
Django's session backend:

```python
from fastapi import Request, HTTPException
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User

def get_current_user(request: Request) -> User:
    session_key = request.cookies.get('sessionid')
    if not session_key:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = SessionStore(session_key=session_key)
    user_id = session.get('_auth_user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")
```

---

## 8. API Endpoints (FastAPI)

All endpoints are served by FastAPI. Use Pydantic models for request/response schemas.
OpenAPI documentation is auto-generated at `/api/docs/` (Swagger UI) and `/api/redoc/`
(ReDoc). (Task DOC1)

### 8.1 Price Endpoints (Owner: Leo)

| Method | Path                          | Description                        |
|--------|-------------------------------|------------------------------------|
| GET    | `/api/prices/{symbol}`        | Get current price for a symbol     |
| GET    | `/api/prices/`                | Get prices for all tracked symbols |

### 8.2 Holding Endpoints (Owner: Paulo)

| Method | Path                          | Description                        |
|--------|-------------------------------|------------------------------------|
| GET    | `/api/holdings/`              | List holdings for current user     |
| POST   | `/api/holdings/`              | Create a new holding               |
| GET    | `/api/holdings/{id}`          | Get holding detail with P&L        |
| PUT    | `/api/holdings/{id}`          | Update holding                     |
| DELETE | `/api/holdings/{id}`          | Remove holding                     |

### 8.3 Portfolio Endpoints (Owner: Rodrigo)

| Method | Path                              | Description                              |
|--------|-----------------------------------|------------------------------------------|
| GET    | `/api/portfolios/`                | List portfolios for current user         |
| POST   | `/api/portfolios/`                | Create a new portfolio                   |
| GET    | `/api/portfolios/{id}`            | Portfolio detail with totals and P&L     |
| GET    | `/api/portfolios/{id}/allocation` | Allocation breakdown                     |
| GET    | `/api/portfolios/{id}/history`    | Performance history (snapshots)          |
| GET    | `/api/portfolios/{id}/alerts`     | List alerts for portfolio                |
| POST   | `/api/portfolios/{id}/alerts`     | Create a new alert                       |

---

## 9. Service Layer (Task A1)

Extract all business logic from models and API routers into dedicated service classes.
Services live in the `services/` directory at project root.

```python
# services/price_service.py
class PriceServiceFacade:
    """Thin wrapper that delegates to apps.apis.services.unified."""
    def get_price(self, symbol: str) -> PriceResult: ...
    def get_all_prices(self) -> dict[str, PriceResult]: ...

# services/holding_service.py
class HoldingService:
    """Business logic for creating, updating, and computing holding metrics."""
    def create_holding(self, portfolio_id, asset_id, quantity, avg_buy_price) -> Holding: ...
    def get_holding_detail(self, holding_id) -> dict: ...

# services/portfolio_service.py
class PortfolioService:
    """Business logic for portfolio aggregations and analytics."""
    def get_portfolio_summary(self, portfolio_id) -> dict: ...
    def get_allocation(self, portfolio_id) -> list[dict]: ...
    def capture_snapshot(self, portfolio_id) -> PortfolioSnapshot: ...
```

Rules:
- Follow Single Responsibility principle. One service per domain concern.
- No business logic in API routers (FastAPI routes). Routers only validate input,
  call services, and return responses.
- No business logic in Django views. Views only render templates.
- Services are independently testable.

---

## 10. Repository Pattern (Task A2)

Abstract all ORM queries into Repository classes. Services and API routers call repositories,
never the ORM directly. Repositories live in the `repositories/` directory at project root.

```python
# repositories/holding_repository.py
class HoldingRepository:
    def get_by_id(self, holding_id: int) -> Holding: ...
    def get_by_portfolio(self, portfolio_id: int) -> QuerySet[Holding]: ...
    def create(self, **kwargs) -> Holding: ...
    def update(self, holding_id: int, **kwargs) -> Holding: ...
    def delete(self, holding_id: int) -> None: ...

# repositories/portfolio_repository.py
class PortfolioRepository:
    def get_holdings(self, portfolio_id: int) -> QuerySet[Holding]: ...
    def get_by_user(self, user_id: int) -> QuerySet[Portfolio]: ...
    def create(self, **kwargs) -> Portfolio: ...

# repositories/alert_repository.py
class AlertRepository:
    def get_active(self, portfolio_id: int) -> QuerySet[Alert]: ...
    def create(self, **kwargs) -> Alert: ...
    def mark_triggered(self, alert_id: int) -> Alert: ...
```

Rules:
- Use `select_related` and `prefetch_related` to avoid N+1 queries.
- Type-annotate all return types.
- Repositories can be swapped for mocks in tests without touching service code.

---

## 11. Settings Architecture (Task A3)

Use split settings: `config/settings/base.py`, `config/settings/dev.py`, `config/settings/prod.py`.
The `DJANGO_SETTINGS_MODULE` env var selects the active settings file.
Default in `.env.example`: `config.settings.dev`.

Use `django-environ` (`environ`) for all environment variable parsing.

### Required .env variables

```
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
COINGECKO_API_KEY=
YAHOO_FINANCE_ENABLED=True
CACHE_TTL_CRYPTO=300
CACHE_TTL_STOCK=600
RETRY_MAX_ATTEMPTS=3
LOG_LEVEL=DEBUG


Here!!!!!!

DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Disable real APIs
USE_MOCK_DATA=True

COINGECKO_BASE_URL=
COINGECKO_API_KEY=
YAHOO_FINANCE_ENABLED=False

CACHE_TTL_CRYPTO=300
CACHE_TTL_STOCK=600
RETRY_MAX_ATTEMPTS=3
LOG_LEVEL=DEBUG
!!!!
```

Rules:
- No hardcoded strings outside the config module.
- Secrets must never appear in `base.py`. Load from env only.
- `prod.py` is stubbed with `DEBUG=False` and stricter `ALLOWED_HOSTS`.
- Document all env vars in `.env.example` with comments.

---

## 12. Requirements

Pin all versions. The `requirements.txt` must include at minimum:

```
Django>=5.0,<6.0
django-environ>=0.11
fastapi>=0.110
uvicorn[standard]>=0.29
pydantic>=2.0
requests>=2.31
yfinance>=0.2
tenacity>=8.2
structlog>=24.0
pytest>=8.0
pytest-django>=4.8
pytest-mock>=3.12
responses>=0.25
model-bakery>=1.18        # Or factory_boy -- pick one for test fixtures
Pillow>=10.0              # Only if ImageField is used anywhere
```

---

## 13. Admin Registration

Every model must be registered in its app's `admin.py`. Use `@admin.register` decorator.

- `Asset`: `list_display = ['symbol', 'name', 'asset_type', 'created_at']`,
  `search_fields = ['symbol', 'name']`, `list_filter = ['asset_type']`
- `Holding`: `list_display = ['asset', 'portfolio', 'quantity', 'avg_buy_price', 'updated_at']`,
  `list_filter = ['asset__asset_type']`, `search_fields = ['asset__symbol']`
- `Portfolio`: `list_display = ['name', 'user', 'created_at']`,
  `search_fields = ['name', 'user__username']`
- `PortfolioSnapshot`: `list_display = ['portfolio', 'date', 'value']`,
  `list_filter = ['date']`, `readonly_fields = ['created_at']`
- `Alert`: `list_display = ['portfolio', 'asset', 'target_price', 'direction', 'active', 'triggered']`,
  `list_filter = ['active', 'triggered', 'direction']`

---

## 14. URL Structure

`config/urls.py` handles Django-served routes only (admin + templates):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.portfolio.urls', namespace='portfolio')),  # Template views
    path('accounts/', include('django.contrib.auth.urls')),           # Built-in auth views
]
```

All `/api/` routes are handled by FastAPI (see Section 8). They are not registered
in Django's `urls.py`.

---

## 15. Frontend Conventions

- Base template: `templates/base.html`. All other templates extend it.
- HTMX is loaded via CDN in `base.html`. Pin the version: `htmx.org@2.0`.
- The frontend is minimal: a dashboard showing portfolio totals, holdings list, and
  basic P&L. HTMX calls hit FastAPI endpoints and swap HTML partials.
- No custom JavaScript files unless explicitly instructed.
- Static files: CSS in `static/css/main.css`. No CSS framework is prescribed -- use
  plain CSS or add one only if explicitly instructed.
- Login/logout uses Django's built-in auth views and templates.

---

## 16. Management Commands

Since Celery is not used, periodic tasks are handled via Django management commands.

### capture_snapshots

```bash
python manage.py capture_snapshots
```

Creates a `PortfolioSnapshot` for every portfolio in the database with today's
`current_value`. Idempotent: if a snapshot for today already exists, it updates
the value. Can be scheduled via cron.

Location: `apps/portfolio/management/commands/capture_snapshots.py`

---

## 17. Testing Strategy

Use `pytest` with `pytest-django` as the test runner. All tests must be runnable with:

```bash
pytest
```

### Coverage targets

Each domain must achieve >80% test coverage:
- `apps/apis/tests/` -- All price service methods, error paths, cache logic, config loading.
  (Task L10, L11)
- `apps/wallet/tests/` -- All holding and asset model methods, formulas, edge cases,
  Decimal checks. Use `@pytest.mark.parametrize` for multiple scenarios. Include zero-qty,
  large numbers, breakeven. (Task P6, P9)
- `apps/portfolio/tests/` -- All portfolio aggregations, snapshot creation, alert queries,
  allocation logic. Test: empty portfolio, single holding, multi-holding, zero-price asset.
  (Task R6, R9)
- `tests/test_integration.py` -- End-to-end flows: POST holding via API, price fetch,
  portfolio aggregation, assert DB state. Use `@pytest.mark.django_db`. Seed fixtures.
  (Task T4)

### Test rules

- All external HTTP calls must be mocked. Tests must pass offline. (Task L11)
- Use `responses` or `pytest-httpretty` for HTTP mocking.
- Use `model_bakery` or `factory_boy` for model fixtures.
- Fixtures stored in `apps/apis/tests/fixtures/` and version-controlled.
- Mock the price service in wallet and portfolio tests.
- CI must pass with coverage report generated.

### pytest configuration

In `pyproject.toml` or `pytest.ini`:

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = config.settings.dev
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers -v
```

---

## 18. Documentation (Tasks DOC1, DOC2, DOC3)

### DOC1: API Documentation

OpenAPI 3.0 spec is auto-generated by FastAPI at `/api/docs/` (Swagger UI) and
`/api/redoc/` (ReDoc). All endpoints must include:
- Clear request/response schemas via Pydantic models.
- Example values in Pydantic `model_config` or `Field(examples=[...])`.
- Authentication requirements documented.

### DOC2: README

Comprehensive `README.md` covering:
- Project description and architecture overview.
- Prerequisites (Python 3.12+, pip).
- Local setup: clone, create venv, install requirements, copy `.env.example`, migrate, seed.
- How to run: Django server + uvicorn for FastAPI.
- How to run tests: `pytest` with coverage.
- Common commands: `makemigrations`, `migrate`, `createsuperuser`, `capture_snapshots`.
- Env var reference.
- Troubleshooting section.
- A new developer should be able to run the project in under 15 minutes following the README.

### DOC3: Architecture Documentation

Markdown documents with diagrams (Mermaid) in `docs/`:
- `architecture.md` -- System overview, component responsibilities, tech stack rationale.
- `data_flow.md` -- Request flow from API call to DB and back, price service data flow,
  service layer interactions.
- Diagrams: DB schema (ER diagram), service layer map, external API integration flow.
- Must be reviewed by all 3 team members. Stored in `/docs` folder.

---

## 19. Execution Order

When bootstrapping the project from scratch, follow this order exactly:

1. Create the repository folder `investsight/`.
2. Create `.env.example`, `.gitignore`, `requirements.txt`.
3. Create `config/` package with split settings. Wire `DJANGO_SETTINGS_MODULE`,
   `SECRET_KEY`, `CACHES`, `SESSION_ENGINE`, `INSTALLED_APPS`, `STATIC_ROOT`.
4. Create `apps/apis/`, `apps/wallet/`, `apps/portfolio/` as Django app packages.
5. Define all models (Section 5). Run `makemigrations` for wallet and portfolio apps.
6. Apply migrations: `python manage.py migrate`.
7. Create the service layer (`services/`) and repository layer (`repositories/`).
8. Create the FastAPI application in `api/` with routers and schemas.
9. Implement price services in `apps/apis/services/` (L1 through L9, in dependency order).
10. Implement wallet model properties and calculations (P1 through P8).
11. Implement portfolio aggregations and analytics (R1 through R8).
12. Register all models in `admin.py` per app.
13. Create `templates/base.html` and minimal template views.
14. Create `tests/` structure and write unit tests per domain (L10, L11, P6, P9, R6, R9).
15. Write integration tests (T4).
16. Create management command `capture_snapshots`.
17. Write `README.md` (DOC2) and architecture docs (DOC3).
18. Verify: `python manage.py migrate` applies all migrations cleanly.
19. Verify: `python manage.py createsuperuser` works and admin lists all models.
20. Verify: `uvicorn api.main:app --reload` starts and `/api/docs/` renders all endpoints.
21. Verify: `pytest` runs all tests and passes with >80% coverage.

---

## 20. Sprint Backlog Reference

The full task breakdown with IDs, owners, acceptance criteria, and dependencies is defined
in the Sprint Backlog PDF. Below is a summary of all task IDs for quick reference:

### Leo (APIs domain): L1 through L11

| ID  | Task                      | Est | Dependencies         |
|-----|---------------------------|-----|----------------------|
| L1  | Mock price function       | 2h  | None                 |
| L2  | Integrate CoinGecko API   | 4h  | L9, L6               |
| L3  | Integrate Yahoo Finance   | 4h  | L9, L6               |
| L4  | Unified price service     | 3h  | L2, L3               |
| L5  | Implement caching         | 3h  | L4, L9               |
| L6  | Error handling & fallback | 3h  | L1, L4               |
| L7  | Rate limit handling       | 3h  | L6, L8               |
| L8  | Logging system            | 2h  | L9                   |
| L9  | API config module         | 2h  | None                 |
| L10 | Unit tests (API layer)    | 4h  | L1 through L9        |
| L11 | Mock external APIs        | 3h  | L10                  |

### Paulo (Wallet domain): P1 through P9

| ID  | Task                        | Est | Dependencies     |
|-----|-----------------------------|-----|------------------|
| P1  | Asset current_price property| 2h  | L4, P8           |
| P2  | Holding.total_cost property | 2h  | P8               |
| P3  | Holding.current_value       | 3h  | P1, P2           |
| P4  | Absolute P&L                | 2h  | P2, P3           |
| P5  | Percentage P&L              | 2h  | P4               |
| P6  | Validate holding calcs      | 3h  | P1 through P5    |
| P7  | Currency normalisation      | 3h  | L4, P8           |
| P8  | Decimal precision           | 2h  | None             |
| P9  | Unit tests (Wallet layer)   | 4h  | P1 through P8    |

### Rodrigo (Portfolio domain): R1 through R9

| ID  | Task                      | Est | Dependencies         |
|-----|---------------------------|-----|----------------------|
| R1  | Total invested            | 2h  | P2, R4               |
| R2  | Current portfolio value   | 3h  | P3, R4               |
| R3  | Total P&L                 | 2h  | R1, R2               |
| R4  | Holdings selector         | 2h  | A2                   |
| R5  | Active alerts             | 2h  | A2                   |
| R6  | Validate portfolio totals | 3h  | R1 through R3        |
| R7  | Performance history       | 4h  | R2, A1               |
| R8  | Allocation breakdown      | 3h  | R2, R4               |
| R9  | Unit tests (Portfolio)    | 4h  | R1 through R8        |

### Shared (Team): A1 through A3, T4, DOC1 through DOC3

| ID   | Task                      | Est | Dependencies              |
|------|---------------------------|-----|---------------------------|
| A1   | Service layer refactor    | 4h  | L4, P-series, R-series    |
| A2   | Repository pattern        | 4h  | A1                        |
| A3   | Settings modularisation   | 2h  | L9                        |
| T4   | Integration tests         | 5h  | A1, A2, all L/P/R         |
| DOC1 | API documentation         | 3h  | A1                        |
| DOC2 | README                    | 2h  | A3                        |
| DOC3 | Architecture docs         | 3h  | A1, A2                    |

---

## 21. Constraints and Non-Goals

- Do NOT install or use: Redis, `django-redis`, or any external cache backend.
- Do NOT install or use: Celery, `django-celery-beat`, or any task queue.
- Do NOT install or use: JWT libraries (`PyJWT`, `djangorestframework-simplejwt`, etc.).
- Do NOT install or use: Django REST Framework. All API endpoints are FastAPI.
- Do NOT install or use: PostgreSQL or any database other than SQLite.
- Do NOT install or use: Docker or Docker Compose.
- Do NOT install or use: `django-allauth`. Built-in auth only.
- Do NOT implement real payment processing of any kind.
- Do NOT implement a custom user model. Use `django.contrib.auth.models.User`.
- All money and quantity values are stored as `DecimalField`, never `FloatField`.
- All primary keys are standard auto-increment integers.
- Never commit `.env` -- only `.env.example`.
- Use Django sessions (DB-backed) for authentication. No token-based auth.
- Periodic tasks (snapshots) use management commands, not Celery.
- The project must run locally without Docker: `manage.py runserver` + `uvicorn`.
