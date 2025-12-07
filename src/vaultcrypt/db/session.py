from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vaultcrypt.config import DB_URL

#create engine and allow sqlite multi-threading
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})

#session factory for DB interactions
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)