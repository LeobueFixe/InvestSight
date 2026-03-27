# Data Flow

## Price Fetching

1. User requests price via API (`/api/prices/{symbol}`)
2. FastAPI router calls `services.price_service`
3. Service calls unified price service
4. Unified service checks cache first
5. If cache miss, fetches from provider (CoinGecko/Yahoo)
6. Result cached and returned

## Portfolio Aggregation

1. User requests portfolio detail
2. Django view calls portfolio service
3. Service iterates holdings, calls price service
4. Calculates total invested, current value, P&L

## Holding CRUD

1. API request to create/update/delete holding
2. Service layer validates and executes
3. Repository handles ORM operations
4. Changes persisted to SQLite
