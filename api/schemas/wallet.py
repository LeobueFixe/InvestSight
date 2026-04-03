from pydantic import BaseModel, Field


class WalletCreate(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class WalletRestore(BaseModel):
    seed_phrase: str = Field(min_length=1)
    password: str = Field(min_length=8, max_length=128)


class WalletCreateResponse(BaseModel):
    id: int
    seed_phrase: str
    message: str = "Store this seed phrase securely. It will not be shown again."


class WalletRestoreResponse(BaseModel):
    id: int
    message: str = "Wallet restored successfully."


class WalletResponse(BaseModel):
    id: int
    created_at: str
