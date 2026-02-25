"""
ArchiveAI – SQLAlchemy ORM table definitions.

These tables persist data that currently lives only in memory:
  • users          – registered phone numbers & preferences
  • sms_messages   – inbound & outbound SMS log
  • ussd_sessions  – USSD session snapshots
  • voice_records  – voice recording metadata + transcriptions
  • search_logs    – every search query & result count
  • doc_requests   – document request queue
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON

from app.database import Base


# ─────────────────────────────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<User {self.phone_number}>"


# ─────────────────────────────────────────────────────────────────────
# SMS Messages
# ─────────────────────────────────────────────────────────────────────

class SMSMessage(Base):
    __tablename__ = "sms_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    at_message_id = Column(String(100), index=True)  # Africa's Talking msg ID
    phone_number = Column(String(20), nullable=False, index=True)
    direction = Column(String(10), nullable=False)  # "inbound" | "outbound"
    text = Column(Text, nullable=False)
    status = Column(String(30), default="sent")  # sent / delivered / failed
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<SMS {self.direction} {self.phone_number}>"


# ─────────────────────────────────────────────────────────────────────
# USSD Session Snapshots
# ─────────────────────────────────────────────────────────────────────

class USSDSessionRecord(Base):
    __tablename__ = "ussd_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    stage = Column(String(30), default="welcome")
    language = Column(String(5), default="en")
    search_query = Column(Text, nullable=True)
    search_results = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<USSDSession {self.session_id}>"


# ─────────────────────────────────────────────────────────────────────
# Voice Recordings
# ─────────────────────────────────────────────────────────────────────

class VoiceRecord(Base):
    __tablename__ = "voice_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    recording_url = Column(Text, nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    transcription = Column(Text, nullable=True)
    language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<VoiceRecord {self.session_id}>"


# ─────────────────────────────────────────────────────────────────────
# Search Logs
# ─────────────────────────────────────────────────────────────────────

class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), nullable=True, index=True)
    query = Column(Text, nullable=False)
    language = Column(String(5), default="en")
    source = Column(String(10), default="ussd")  # ussd | sms | voice | api
    result_count = Column(Integer, default=0)
    elapsed_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<SearchLog '{self.query[:30]}'>"


# ─────────────────────────────────────────────────────────────────────
# Document Requests
# ─────────────────────────────────────────────────────────────────────

class DocumentRequest(Base):
    __tablename__ = "document_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), nullable=False, index=True)
    doc_id = Column(String(100), nullable=False, index=True)
    doc_title = Column(Text, nullable=True)
    status = Column(String(30), default="pending")  # pending | ready | collected
    notification_sent = Column(Boolean, default=False)
    language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<DocRequest {self.doc_id} → {self.phone_number}>"
