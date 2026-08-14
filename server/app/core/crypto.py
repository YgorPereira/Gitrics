from cryptography.fernet import Fernet

from app.core import settings

_fernet = Fernet(settings.FERNET_SECRET_KEY)


def encrypt_token(token: str) -> str:
    return _fernet.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return _fernet.decrypt(encrypted_token.encode()).decode()
