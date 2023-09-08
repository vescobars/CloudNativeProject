from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.constants import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

Base = declarative_base()

# Dependency
def get_session():
    """Shares a single db session to be used throughout the service"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()