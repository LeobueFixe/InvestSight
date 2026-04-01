import os
import base64
import hashlib
from typing import Tuple

from mnemonic import Mnemonic
from cryptography.fernet import Fernet

from apps.wallet.models import Wallet


class WalletService:
    WORDS = 12
    PASSPHRASE = ""

    def __init__(self):
        self.mnemo = Mnemonic("english")

    def generate_seed_phrase(self) -> str:
        return self.mnemo.generate(strength=128)

    def validate_seed_phrase(self, seed_phrase: str) -> bool:
        return self.mnemo.check(seed_phrase)

    def seed_to_bytes(self, seed_phrase: str) -> bytes:
        return self.mnemo.to_seed(seed_phrase, passphrase=self.PASSPHRASE)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            100000,
            dklen=32,
        )

    def _encrypt_seed(self, seed_bytes: bytes, password: str) -> bytes:
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        fernet_key = base64.urlsafe_b64encode(key)
        fernet = Fernet(fernet_key)

        salt_and_encrypted = salt + fernet.encrypt(seed_bytes)
        return salt_and_encrypted

    def _decrypt_seed(self, encrypted_data: bytes, password: str) -> bytes:
        salt = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        key = self._derive_key(password, salt)
        fernet_key = base64.urlsafe_b64encode(key)
        fernet = Fernet(fernet_key)
        return fernet.decrypt(encrypted)

    def create_wallet(self, user, password: str) -> Tuple[Wallet, str]:
        seed_phrase = self.generate_seed_phrase()
        seed_bytes = self.seed_to_bytes(seed_phrase)
        encrypted_seed = self._encrypt_seed(seed_bytes, password)

        wallet = Wallet.objects.create(
            user=user,
            encrypted_seed=encrypted_seed,
        )
        return wallet, seed_phrase

    def restore_wallet(self, user, seed_phrase: str, password: str) -> Wallet:
        if not self.validate_seed_phrase(seed_phrase):
            raise ValueError("Invalid seed phrase")

        seed_bytes = self.seed_to_bytes(seed_phrase)
        encrypted_seed = self._encrypt_seed(seed_bytes, password)

        wallet, _ = Wallet.objects.update_or_create(
            user=user,
            defaults={"encrypted_seed": encrypted_seed},
        )
        return wallet

    def decrypt_seed_phrase(self, wallet: Wallet, password: str) -> str:
        seed_bytes = self._decrypt_seed(wallet.encrypted_seed, password)
        return self.mnemo.to_mnemonic(seed_bytes)

    def get_wallet(self, user):
        return Wallet.objects.filter(user=user).first()
