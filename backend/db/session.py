from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from ..core.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables in the database"""
    Base.metadata.drop_all(bind=engine)
