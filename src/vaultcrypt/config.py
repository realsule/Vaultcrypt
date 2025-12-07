from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables


BASE_DIR = Path(__file__).resolve().parent.parent

# DB connection
DB_URL = os.getenv('DB_URL', f'sqlite:///{BASE_DIR / "vault.db"}')

# Master key for encryption/decryption
MASTER_KEY = os.getenv('MASTER_KEY')

# File encryption key path
FILE_KEY_PATH = os.getenv('FILE_KEY_PATH', str(BASE_DIR / 'filekey.key'))


# For safety, warn if no key (we still allow local dev fallback for tests)
if not MASTER_KEY:
    MASTER_KEY = os.getenv('MASTER_KEY_FALLBACK')