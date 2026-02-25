"""
ArchiveAI – Pydantic models for USSD sessions, SMS messages,
voice recordings, search requests, and AI service payloads.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────

class USSDStage(str, Enum):
    """Tracks the current stage of a USSD session."""
    WELCOME = "welcome"
    LANGUAGE_SELECT = "language_select"
    MAIN_MENU = "main_menu"
    SEARCH_INPUT = "search_input"
    SEARCH_RESULTS = "search_results"
    DOCUMENT_DETAIL = "document_detail"
    REQUEST_DOCUMENT = "request_document"
    CONFIRMATION = "confirmation"


class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class VoiceStatus(str, Enum):
    RINGING = "ringing"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no-answer"
    BUSY = "busy"


class NotificationType(str, Enum):
    SEARCH_RESULT = "search_result"
    DOCUMENT_READY = "document_ready"
    RESERVATION_CONFIRM = "reservation_confirm"
    REMINDER = "reminder"


# ─────────────────────────────────────────────────────────────────────
# USSD
# ─────────────────────────────────────────────────────────────────────

class USSDRequest(BaseModel):
    """Inbound POST payload from Africa's Talking USSD gateway."""
    sessionId: str
    serviceCode: str
    phoneNumber: str
    text: str  # cumulative *-separated user input


class USSDSession(BaseModel):
    """In-memory session state for one USSD conversation."""
    session_id: str
    phone_number: str
    stage: USSDStage = USSDStage.WELCOME
    language: str = "en"
    search_query: Optional[str] = None
    search_results: List[Dict[str, Any]] = Field(default_factory=list)
    selected_doc_index: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    extra: Dict[str, Any] = Field(default_factory=dict)

    def touch(self) -> None:
        """Update the last-activity timestamp."""
        self.updated_at = datetime.utcnow()


# ─────────────────────────────────────────────────────────────────────
# SMS
# ─────────────────────────────────────────────────────────────────────

class InboundSMS(BaseModel):
    """Inbound SMS callback from Africa's Talking."""
    date: str  # e.g. "2026-02-25 12:00:00"
    from_: str = Field(..., alias="from")  # sender phone
    id: str  # AT message id
    linkId: Optional[str] = None
    text: str
    to: str  # shortcode / phone number
    networkCode: Optional[str] = None

    class Config:
        populate_by_name = True


class OutboundSMS(BaseModel):
    """Payload for sending an SMS via Africa's Talking."""
    to: List[str]  # recipient phone numbers
    message: str
    from_: Optional[str] = Field(None, alias="from")  # sender ID / shortcode
    enqueue: bool = True

    class Config:
        populate_by_name = True


class SMSDeliveryReport(BaseModel):
    """Delivery status callback from Africa's Talking."""
    id: str
    status: str
    phoneNumber: str
    networkCode: Optional[str] = None
    failureReason: Optional[str] = None
    retryCount: Optional[int] = None


# ─────────────────────────────────────────────────────────────────────
# Voice
# ─────────────────────────────────────────────────────────────────────

class VoiceCallback(BaseModel):
    """Inbound voice callback from Africa's Talking."""
    sessionId: str
    callerNumber: str
    destinationNumber: str
    isActive: str  # "0" or "1"
    direction: Optional[str] = None
    callStartTime: Optional[str] = None
    callerCountryCode: Optional[str] = None
    dtmfDigits: Optional[str] = None
    recordingUrl: Optional[str] = None
    durationInSeconds: Optional[str] = None
    currencyCode: Optional[str] = None
    amount: Optional[str] = None


class VoiceRecording(BaseModel):
    """Metadata for a captured voice recording."""
    session_id: str
    phone_number: str
    recording_url: str
    duration_seconds: Optional[int] = None
    transcription: Optional[str] = None
    language: str = "en"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────────────────────────────
# AI / Search Service
# ─────────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    """Payload sent to the AI search micro-service."""
    query: str
    language: str = "en"
    top_k: int = 5
    filters: Dict[str, Any] = Field(default_factory=dict)


class DocumentResult(BaseModel):
    """A single document result returned by the AI service."""
    doc_id: str
    title: str
    snippet: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    language: Optional[str] = None


class SearchResponse(BaseModel):
    """Response envelope from the AI search service."""
    query: str
    results: List[DocumentResult] = Field(default_factory=list)
    total_found: int = 0
    elapsed_ms: Optional[float] = None


class DocumentRequestPayload(BaseModel):
    """User requests a physical/digital copy of a document."""
    phone_number: str
    doc_id: str
    notification_type: NotificationType = NotificationType.DOCUMENT_READY
    language: str = "en"


# ─────────────────────────────────────────────────────────────────────
# Generic API Responses
# ─────────────────────────────────────────────────────────────────────

class APIResponse(BaseModel):
    """Standard JSON envelope for REST endpoints."""
    success: bool
    message: str = ""
    data: Optional[Any] = None
