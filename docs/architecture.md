# InvestSight Architecture

## Overview

InvestSight is a crypto and stock portfolio tracker built with Django and FastAPI.

## Components

### Django Applications

- **apps.apis** (Leo): Price fetching services
- **apps.wallet** (Paulo): Asset and Holding models
- **apps.portfolio** (Rodrigo): Portfolio aggregations

### Service Layer

Located in `services/`:
- `price_service.py` - Price facade
- `holding_service.py` - Holding business logic
- `portfolio_service.py` - Portfolio aggregations

### Repository Layer

Located in `repositories/`:
- `holding_repository.py`
- `portfolio_repository.py`
- `alert_repository.py`

### API Layer

FastAPI application in `api/` with routers for prices, holdings, portfolios, and alerts.

## Technology Stack

- Django 5.x for ORM, admin, templates
- FastAPI for REST API endpoints
- SQLite for database
- LocMemCache for caching
