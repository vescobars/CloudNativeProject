""" SQLAlchemy's configuration for Postgres connection """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@0.0.0.0:5432/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

Base = declarative_base()


# Dependency
def get_session():
    """Shares a single db session to be used throughout the service"""
    session = Session()
    print("Tried to get session")
    try:
        yield session
    finally:
        session.close()
