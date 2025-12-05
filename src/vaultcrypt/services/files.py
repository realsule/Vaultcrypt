from cryptography.fernet import Fernet
from pathlib import Path
from typing import Optional, List
from vaultcrypt.config import FILE_KEY_PATH
import os


def generate_file_key(path: Optional[str] = None) -> bytes:
    key = Fernet.generate_key()
    p = Path(path or FILE_KEY_PATH)
    p.write_bytes(key)
    return key


def load_file_key(path: Optional[str] = None) -> bytes:
    p = Path(path or FILE_KEY_PATH)
    if not p.exists():
        raise FileNotFoundError('File key not found. Run generate_file_key first.')
    return p.read_bytes()


def _cipher_from_key(key: bytes):
    return Fernet(key)


def encrypt_file(path: str, key: Optional[bytes] = None, out_path: Optional[str] = None) -> str:
    p = Path(path)
    key = key or load_file_key()
    cipher = _cipher_from_key(key)
    data = p.read_bytes()
    token = cipher.encrypt(data)
    out = Path(out_path or (str(p) + '.enc'))
    out.write_bytes(token)
    return str(out)


def decrypt_file(path: str, key: Optional[bytes] = None, out_path: Optional[str] = None) -> str:
    p = Path(path)
    key = key or load_file_key()
    cipher = _cipher_from_key(key)
    token = p.read_bytes()
    data = cipher.decrypt(token)
    if out_path:
        out = Path(out_path)
    else:
        if str(p).endswith('.enc'):
            out = Path(str(p)[:-4])
        else:
            out = Path(str(p) + '.dec')
    out.write_bytes(data)
    return str(out)


def bulk_encrypt_folder(folder: str, key: Optional[bytes] = None, pattern: str = '*') -> List[str]:
    p = Path(folder)
    key = key or load_file_key()
    files = [str(fp) for fp in p.glob(pattern) if fp.is_file()]
    out_files = []
    for f in files:
        out_files.append(encrypt_file(f, key=key))
    return out_files