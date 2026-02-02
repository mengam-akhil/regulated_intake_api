from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
DATABASE_URL = "sqlite:///./regtech.db"  # or your DB

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # only for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ✅ REQUIRED BY FASTAPI DEPENDENCY INJECTION
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
