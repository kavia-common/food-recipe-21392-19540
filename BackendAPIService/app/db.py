import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment with defaults."""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()

class Base(DeclarativeBase):
    """Base for SQLAlchemy models."""

_engine = None
_SessionLocal = None

def _engine_and_session():
    global _engine, _SessionLocal
    if _engine is None or _SessionLocal is None:
        settings = get_settings()
        connect_args = {}
        url = settings.DATABASE_URL
        if url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        _engine = create_engine(url, echo=False, future=True, connect_args=connect_args)
        _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False, class_=Session)
    return _engine, _SessionLocal

# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session, closing it after use."""
    _, SessionLocal = _engine_and_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PUBLIC_INTERFACE
def init_db():
    """Create tables if they do not exist."""
    engine, _ = _engine_and_session()
    from .models import Recipe, Image, Menu, recipe_menu  # noqa: F401
    Base.metadata.create_all(bind=engine)
