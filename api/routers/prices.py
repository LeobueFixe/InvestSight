from fastapi import APIRouter, HTTPException

from api.schemas.price import PriceResponse, PriceListResponse
from services.price_service import get_price_service

router = APIRouter()


@router.get("/{symbol}", response_model=PriceResponse)
async def get_price(symbol: str):
    service = get_price_service()
    result = service.get_price(symbol.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return PriceResponse(
        symbol=result.symbol,
        price=result.price,
        currency=result.currency,
        provider=result.provider,
        timestamp=result.timestamp,
    )


@router.get("/", response_model=PriceListResponse)
async def get_all_prices():
    service = get_price_service()
    results = service.get_all_prices()
    return PriceListResponse(prices=results)
