# InvestSight

A crypto and stock portfolio tracker built with **Django 5** + **FastAPI**, developed as a Backend I capstone project.

---

## Team

| Member  | Domain      | Responsibility                                                      |
|---------|-------------|---------------------------------------------------------------------|
| Leo     | APIs        | Price fetching, caching, error handling, rate limits, logging       |
| Paulo   | Wallet      | Asset & Holding models, P&L calculations, decimal precision         |
| Rodrigo | Portfolio   | Portfolio aggregations, alerts, snapshots, allocation breakdowns    |

---

## Tech Stack

| Layer              | Technology                                  |
|--------------------|---------------------------------------------|
| Web framework      | Django 5.x – ORM, admin, templates, sessions |
| API framework      | FastAPI – all REST endpoints                |
| Language           | Python 3.12+                                |
| Database           | SQLite (Django ORM)                         |
| Cache              | Django `LocMemCache`                        |
| HTTP client        | `requests`                                  |
| Finance data       | CoinGecko API + `yfinance` (Yahoo Finance)  |
| Retry logic        | `tenacity` (exponential backoff)            |
| Structured logging | `structlog` (JSON)                          |
| Environment config | `django-environ`                            |
| Testing            | `pytest` + `pytest-django` + `pytest-mock`  |
| Frontend           | Django Templates + HTMX + Chart.js          |

---

## Project Structure

```
investsight/
├── manage.py
├── requirements.txt
├── pyproject.toml
├── config/                    # Django project settings
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── apps/
│   ├── apis/                  # Leo — price fetching services
│   │   ├── services/
│   │   │   ├── base.py        # PriceService ABC + PriceResult dataclass
│   │   │   ├── mock.py        # Static mock provider
│   │   │   ├── coingecko.py   # CoinGecko integration
│   │   │   ├── yahoo.py       # Yahoo Finance integration
│   │   │   ├── unified.py     # Unified get_price() router
│   │   │   ├── cache.py       # Django cache wrapper
│   │   │   ├── retry.py       # Rate limit handling (tenacity)
│   │   │   └── logging.py     # Structured JSON logging
│   │   └── tests/
│   ├── wallet/                # Paulo — holdings & calculations
│   │   ├── models.py          # Asset, Holding models
│   │   └── tests/
│   └── portfolio/             # Rodrigo — aggregations & analytics
│       ├── models.py          # Portfolio, PortfolioSnapshot, Alert
│       ├── management/
│       │   └── commands/
│       │       └── capture_snapshots.py
│       └── tests/
├── repositories/              # Repository pattern (ORM abstraction)
│   ├── holding_repository.py
│   ├── portfolio_repository.py
│   └── alert_repository.py
├── services/                  # Shared service layer
│   ├── price_service.py
│   ├── holding_service.py
│   └── portfolio_service.py
├── api/                       # FastAPI application
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── prices.py
│   │   ├── holdings.py
│   │   ├── portfolios.py
│   │   └── alerts.py
│   └── schemas/
├── templates/                 # Django HTML templates (HTMX frontend)
├── static/css/
└── tests/
    └── test_integration.py
```

---

## Getting Started

### Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
git clone https://github.com/RodrigoDias123/InvestSight.git
cd InvestSight

# Install dependencies
uv sync
# or: pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Apply migrations
uv run python manage.py migrate

# Create a superuser (optional, for admin)
uv run python manage.py createsuperuser
```

### Running

Two servers need to run simultaneously:

```bash
# Terminal 1 — Django (frontend + admin)
uv run python manage.py runserver 8000

# Terminal 2 — FastAPI (REST API)
uv run uvicorn api.main:app --reload --port 8001
```

| Service        | URL                              |
|----------------|----------------------------------|
| Frontend       | http://localhost:8000            |
| Django Admin   | http://localhost:8000/admin      |
| FastAPI Swagger| http://localhost:8001/api/docs   |
| FastAPI ReDoc  | http://localhost:8001/api/redoc  |

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Set to True to skip real API calls and use static mock prices
USE_MOCK_DATA=False

COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
COINGECKO_API_KEY=your-key-here
YAHOO_FINANCE_ENABLED=True

CACHE_TTL_CRYPTO=300
CACHE_TTL_STOCK=600
RETRY_MAX_ATTEMPTS=3
LOG_LEVEL=DEBUG
```

---

## API Endpoints

All endpoints served by FastAPI at port **8001**.

### Prices

| Method | Path                    | Description                    |
|--------|-------------------------|--------------------------------|
| GET    | `/api/prices/{symbol}`  | Live price for a symbol        |
| GET    | `/api/prices/`          | Prices for all tracked symbols |

### Holdings

| Method | Path                  | Description                      |
|--------|-----------------------|----------------------------------|
| GET    | `/api/holdings/`      | List holdings for current user   |
| POST   | `/api/holdings/`      | Create a new holding             |
| GET    | `/api/holdings/{id}`  | Holding detail with P&L          |
| PUT    | `/api/holdings/{id}`  | Update holding                   |
| DELETE | `/api/holdings/{id}`  | Remove holding                   |

### Portfolios

| Method | Path                                   | Description                      |
|--------|----------------------------------------|----------------------------------|
| GET    | `/api/portfolios/`                     | List portfolios for current user |
| POST   | `/api/portfolios/`                     | Create a new portfolio           |
| GET    | `/api/portfolios/{id}`                 | Detail with totals and P&L       |
| GET    | `/api/portfolios/{id}/allocation`      | Allocation breakdown             |
| GET    | `/api/portfolios/{id}/history`         | Performance history (snapshots)  |
| GET    | `/api/portfolios/{id}/alerts`          | List alerts for portfolio        |
| POST   | `/api/portfolios/{id}/alerts`          | Create a new alert               |

---

## Data Models

### Wallet (`apps/wallet/models.py`)

**Asset**
- `symbol` — unique ticker (e.g. `BTC`, `AAPL`), always uppercase
- `name` — full name
- `asset_type` — `crypto` or `stock`
- `current_price` — property, fetches live price from unified service

**Holding**
- `portfolio` → FK to Portfolio
- `asset` → FK to Asset
- `quantity`, `avg_buy_price` — `DecimalField(max_digits=20, decimal_places=8)`
- `total_cost` — property: `quantity × avg_buy_price`
- `current_value` — property: `quantity × asset.current_price`
- `profit_loss` — property: `current_value − total_cost`
- `pnl_pct` — property: `(profit_loss / total_cost) × 100`

### Portfolio (`apps/portfolio/models.py`)

**Portfolio**
- `name`, `user` (FK to Django User)
- `total_invested` — ORM aggregate `Sum(quantity × avg_buy_price)`
- `current_value` — sum of all `Holding.current_value`
- `total_pnl` — returns `{"absolute": Decimal, "percentage": Decimal}`
- `allocation_breakdown` — list of `{asset, value, pct_of_portfolio}`

**PortfolioSnapshot**
- `portfolio`, `date`, `value`
- Unique together `(portfolio, date)` — one snapshot per day
- DB index on `date`

**Alert**
- `portfolio`, `asset`, `target_price`, `direction` (`above`/`below`)
- `active`, `triggered`, `triggered_at`
- Index on `(portfolio, active)`

---

## Management Commands

```bash
# Capture daily portfolio snapshots (run via cron or manually)
uv run python manage.py capture_snapshots
```

Idempotent — if today's snapshot already exists, it updates the value.

---

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=apps --cov=services --cov=repositories --cov-report=term-missing

# Run per domain
uv run pytest apps/apis/tests/
uv run pytest apps/portfolio/tests/
uv run pytest apps/wallet/tests/
```

### Test Summary

| Domain      | Tests | Status  | Notes                                      |
|-------------|-------|---------|--------------------------------------------|
| `apps/apis` | 20    | 13 ✅ 7 ❌ | Cache, retry, unified, yahoo have failures |
| `apps/portfolio` | 55 | 55 ✅  | All passing                               |
| `apps/wallet`    | 18 | 18 ✅  | All passing                               |
| **Total**   | **95**| **86 ✅ 7 ❌** |                                      |

#### Known failing tests (`apps/apis`)

| Test | Reason |
|------|--------|
| `test_cache.py` — 2 tests | Cache key/TTL mismatch with current implementation |
| `test_retry.py` — 1 test  | `AttributeError` in retry decorator mock           |
| `test_unified.py` — 2 tests | Mock mode flag not being picked up in test env   |
| `test_yahoo.py` — 2 tests   | `yfinance` response schema changed                |

> `apps/apis/tests/test_config.py` has a **collection error** and is excluded from the default run.

---

## Architecture Overview

```
Browser / HTMX
      │
      ▼
Django (port 8000)          FastAPI (port 8001)
  Templates                   REST API endpoints
  Auth / Sessions             Pydantic schemas
      │                             │
      └────────────┬────────────────┘
                   │
          Service Layer (services/)
                   │
          Repository Layer (repositories/)
                   │
          Django ORM + SQLite
```

**Price data flow:**
```
Request → UnifiedPriceService
              ├── Cache hit? → return cached PriceResult
              ├── CoinGecko (BTC, ETH, XRP, SOL, …)
              ├── Yahoo Finance (AAPL, TSLA, MSFT, …)
              └── Fallback → last saved JSON → Mock
```

---

## Supported Assets

**Crypto (CoinGecko):** BTC, ETH, USDT, USDC, BNB, XRP, ADA, DOGE, SOL, DOT, TRX, MATIC, LTC, BCH, LINK, XLM, ATOM, ETC, XMR, ALGO, ICP, FIL, APT, ARB, OP, AVAX, NEAR, HBAR, VET, AAVE, SAND, MANA, EGLD, XTZ, FTM, GRT, RUNE, KSM, CAKE, QNT, FLOW, CHZ, CRV, DYDX

**Stocks (Yahoo Finance):** AAPL, TSLA, MSFT, AMZN, NVDA, META, GOOGL, NFLX, JPM, V, MA, BAC, KO, PEP, DIS




