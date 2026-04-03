from fastapi import APIRouter, HTTPException, Depends

from api.schemas.wallet import (
    WalletCreate,
    WalletRestore,
    WalletCreateResponse,
    WalletRestoreResponse,
    WalletResponse,
)
from api.dependencies import get_current_user
from services.wallet_service import WalletService
from apps.wallet.models import Wallet
from django.contrib.auth.models import User

router = APIRouter()


@router.post("/create", response_model=WalletCreateResponse)
async def create_wallet(data: WalletCreate, user: User = Depends(get_current_user)):
    existing = WalletService().get_wallet(user)
    if existing:
        raise HTTPException(status_code=400, detail="Wallet already exists")

    service = WalletService()
    wallet, seed_phrase = service.create_wallet(user, data.password)

    return WalletCreateResponse(
        id=wallet.id,
        seed_phrase=seed_phrase,
    )


@router.post("/restore", response_model=WalletRestoreResponse)
async def restore_wallet(data: WalletRestore, user: User = Depends(get_current_user)):
    service = WalletService()

    try:
        wallet = service.restore_wallet(user, data.seed_phrase, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return WalletRestoreResponse(id=wallet.id)


@router.get("/", response_model=WalletResponse | None)
async def get_wallet(user: User = Depends(get_current_user)):
    wallet = WalletService().get_wallet(user)
    if not wallet:
        return None

    return WalletResponse(
        id=wallet.id,
        created_at=wallet.created_at.isoformat(),
    )
