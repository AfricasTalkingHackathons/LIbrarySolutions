"""
ArchiveAI – Database engine & session factory.

Uses SQLAlchemy 2.0 async engine with asyncpg driver for Neon PostgreSQL.
Provides:
  • async engine
  • async session factory (for request-scoped sessions)
  • init_db()  – creates all tables
  • get_db()   – FastAPI dependency for DB sessions
"""

from __future__ import annotations

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger(__name__)


# ── Convert the standard postgres:// URL to async asyncpg:// ────────

def _make_async_url(url: str) -> str:
    """
    Convert  postgresql://…  →  postgresql+asyncpg://…
    Strip params that asyncpg doesn't understand (channel_binding, sslmode)
    and convert sslmode=require → ssl=require for asyncpg.
    """
    import re

    async_url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # asyncpg uses `ssl` not `sslmode`
    async_url = re.sub(r"sslmode=require", "ssl=require", async_url)

    # asyncpg doesn't recognise channel_binding – drop it
    async_url = re.sub(r"[&?]channel_binding=[^&]*", "", async_url)

    # clean up trailing ? or &
    async_url = re.sub(r"[?&]+$", "", async_url)
    return async_url


ASYNC_DATABASE_URL = _make_async_url(settings.DATABASE_URL)

# ── Engine ───────────────────────────────────────────────────────────

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# ── Session factory ──────────────────────────────────────────────────

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Declarative Base ─────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── FastAPI dependency ───────────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield one DB session per request; auto-close on completion."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Table creation ───────────────────────────────────────────────────

async def init_db() -> None:
    """Create all tables defined on Base.metadata (idempotent)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created / verified.")


async def close_db() -> None:
    """Dispose of the connection pool."""
    await engine.dispose()
    logger.info("Database connection pool closed.")
