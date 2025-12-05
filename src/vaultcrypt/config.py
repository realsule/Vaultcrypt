from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
DB_URL = os.getenv('DB_URL', f'sqlite:///{BASE_DIR / "vault.db"}')
MASTER_KEY = os.getenv('MASTER_KEY')
FILE_KEY_PATH = os.getenv('FILE_KEY_PATH', str(BASE_DIR / 'filekey.key'))


# For safety, warn if no key (we still allow local dev fallback for tests)
if not MASTER_KEY:
    MASTER_KEY = os.getenv('MASTER_KEY_FALLBACK')