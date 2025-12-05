from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vaultcrypt.config import DB_URL


engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)