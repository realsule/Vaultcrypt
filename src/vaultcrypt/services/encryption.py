from cryptography.fernet import Fernet, InvalidToken
from vaultcrypt.config import MASTER_KEY

if not MASTER_KEY:
    raise RuntimeError('MASTER_KEY is required — set environment variable')

fernet = Fernet(MASTER_KEY.encode() if isinstance(MASTER_KEY, str) else MASTER_KEY)


def encrypt_bytes(data: bytes) -> bytes:
    return fernet.encrypt(data)# encrypt raw bytes


def decrypt_bytes(token: bytes) -> bytes:
    try:
        return fernet.decrypt(token)
    except InvalidToken as e:
        raise ValueError('Invalid encryption token or wrong MASTER_KEY') from e


def encrypt_text(text: str) -> bytes:
    return encrypt_bytes(text.encode('utf-8'))# encrypt string as bytes


def decrypt_text(token: bytes) -> str:
    return decrypt_bytes(token).decode('utf-8')# decrypt back to string