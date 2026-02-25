"""
ArchiveAI – User Session Manager

Manages in-memory USSD sessions with TTL-based expiration.
In production, swap the in-memory store for Redis / PostgreSQL.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Dict, Optional

from app.config import settings
from app.models.models import USSDSession, USSDStage

logger = logging.getLogger(__name__)


class SessionManager:
    """Thread-safe in-memory session store with TTL expiry."""

    def __init__(self, ttl_seconds: int | None = None) -> None:
        self._store: Dict[str, USSDSession] = {}
        self._ttl = ttl_seconds or settings.SESSION_TTL_SECONDS

    # ── Public API ───────────────────────────────────────────────────

    def get_or_create(self, session_id: str, phone_number: str) -> USSDSession:
        """Return existing session or create a new one."""
        self._purge_expired()
        session = self._store.get(session_id)
        if session is None:
            session = USSDSession(
                session_id=session_id,
                phone_number=phone_number,
            )
            self._store[session_id] = session
            logger.info("New session %s for %s", session_id, phone_number)
        else:
            session.touch()
        return session

    def get(self, session_id: str) -> Optional[USSDSession]:
        """Retrieve a session by ID, or None if expired / missing."""
        self._purge_expired()
        session = self._store.get(session_id)
        if session:
            session.touch()
        return session

    def update(self, session: USSDSession) -> None:
        """Persist updated session state."""
        session.touch()
        self._store[session.session_id] = session

    def reset(self, session_id: str) -> None:
        """Reset a session to the welcome stage (keeps phone number)."""
        session = self._store.get(session_id)
        if session:
            session.stage = USSDStage.WELCOME
            session.search_query = None
            session.search_results = []
            session.selected_doc_index = None
            session.touch()

    def delete(self, session_id: str) -> None:
        """Remove a session completely."""
        self._store.pop(session_id, None)

    def active_count(self) -> int:
        """Return number of active (non-expired) sessions."""
        self._purge_expired()
        return len(self._store)

    # ── Internal ─────────────────────────────────────────────────────

    def _purge_expired(self) -> None:
        """Remove sessions that have exceeded the TTL."""
        now = datetime.utcnow()
        expired = [
            sid
            for sid, sess in self._store.items()
            if (now - sess.updated_at).total_seconds() > self._ttl
        ]
        for sid in expired:
            logger.debug("Purging expired session %s", sid)
            del self._store[sid]


# Singleton used across the application
session_manager = SessionManager()
