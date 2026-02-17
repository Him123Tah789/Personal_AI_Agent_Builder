from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Using psycopg2 for sync connection as per request
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Single source of truth for Base — imported from base_class
from app.db.base_class import Base  # noqa: F401

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

