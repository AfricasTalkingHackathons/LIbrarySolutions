"""
ArchiveAI – API Routes

FastAPI application with endpoints for:
  • USSD callback         POST /ussd
  • SMS inbound callback  POST /sms/incoming
  • SMS delivery report   POST /sms/delivery
  • SMS send              POST /sms/send
  • Voice callback        POST /voice
  • AI search (HTTP)      POST /api/search
  • Document request      POST /api/documents/request
  • Health check          GET  /health
  • Session stats         GET  /admin/sessions
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, Response

from app.config import settings
from app.database import close_db, init_db
from app.models.models import (
    APIResponse,
    DocumentRequestPayload,
    InboundSMS,
    NotificationType,
    OutboundSMS,
    SearchRequest,
    SMSDeliveryReport,
    USSDRequest,
    VoiceCallback,
)

# Import DB models so they register with Base.metadata
import app.models.db_models  # noqa: F401

from app.services.ai_service import ai_router
from app.services.session_manager import session_manager
from app.services.sms_service import (
    handle_delivery_report,
    handle_inbound_sms,
    send_notification,
    send_sms,
)
from app.services.ussd_handler import handle_ussd
from app.services.voice_handler import handle_voice_callback

logger = logging.getLogger(__name__)

# ── FastAPI app ──────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent Digitization & Search for African Libraries",
    version="0.1.0",
)


# ── Startup / Shutdown ───────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.info("ArchiveAI starting — %s", settings.APP_NAME)

    # Create database tables (idempotent)
    await init_db()
    logger.info("Database connected & tables ready.")


@app.on_event("shutdown")
async def shutdown():
    await close_db()
    logger.info("ArchiveAI shutdown complete.")


# =====================================================================
# USSD
# =====================================================================

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(""),
):
    """
    Africa's Talking USSD callback.

    AT sends form-encoded data; we return a plain-text response
    prefixed with CON (continue) or END (terminate).
    """
    req = USSDRequest(
        sessionId=sessionId,
        serviceCode=serviceCode,
        phoneNumber=phoneNumber,
        text=text,
    )
    response_text = await handle_ussd(req)
    return PlainTextResponse(content=response_text)


# =====================================================================
# SMS
# =====================================================================

@app.post("/sms/incoming")
async def sms_incoming_callback(
    date: str = Form(""),
    id: str = Form(""),
    linkId: Optional[str] = Form(None),
    text: str = Form(""),
    to: str = Form(""),
    networkCode: Optional[str] = Form(None),
    request: Request = None,
):
    """
    Africa's Talking inbound SMS callback.

    The `from` field is a reserved keyword in Python so we
    extract it manually from form data.
    """
    form = await request.form()
    from_number = form.get("from", "")
    sms = InboundSMS(
        date=date,
        **{"from": from_number},
        id=id,
        linkId=linkId,
        text=text,
        to=to,
        networkCode=networkCode,
    )
    result = await handle_inbound_sms(sms)
    return APIResponse(success=True, message="Processed", data=result)


@app.post("/sms/delivery")
async def sms_delivery_callback(request: Request):
    """Africa's Talking SMS delivery report callback."""
    form_data = await request.form()
    report = dict(form_data)
    handle_delivery_report(report)
    return APIResponse(success=True, message="Delivery report received")


@app.post("/sms/send")
async def sms_send(payload: OutboundSMS):
    """Programmatic endpoint to send an SMS."""
    result = send_sms(
        recipients=payload.to,
        message=payload.message,
        sender=payload.from_,
    )
    return APIResponse(success=True, message="SMS queued", data=result)


# =====================================================================
# Voice
# =====================================================================

@app.post("/voice", response_class=PlainTextResponse)
async def voice_callback(
    sessionId: str = Form(...),
    callerNumber: str = Form(""),
    destinationNumber: str = Form(""),
    isActive: str = Form("1"),
    direction: Optional[str] = Form(None),
    callStartTime: Optional[str] = Form(None),
    callerCountryCode: Optional[str] = Form(None),
    dtmfDigits: Optional[str] = Form(None),
    recordingUrl: Optional[str] = Form(None),
    durationInSeconds: Optional[str] = Form(None),
    currencyCode: Optional[str] = Form(None),
    amount: Optional[str] = Form(None),
):
    """
    Africa's Talking voice callback.

    Returns XML that controls call flow (say, getDigits, record, etc.).
    """
    cb = VoiceCallback(
        sessionId=sessionId,
        callerNumber=callerNumber,
        destinationNumber=destinationNumber,
        isActive=isActive,
        direction=direction,
        callStartTime=callStartTime,
        callerCountryCode=callerCountryCode,
        dtmfDigits=dtmfDigits,
        recordingUrl=recordingUrl,
        durationInSeconds=durationInSeconds,
        currencyCode=currencyCode,
        amount=amount,
    )
    xml_resp = await handle_voice_callback(cb)
    return Response(content=xml_resp, media_type="application/xml")


# =====================================================================
# AI / Search – HTTP API (non-USSD clients)
# =====================================================================

@app.post("/api/search")
async def api_search(body: SearchRequest):
    """Direct HTTP semantic search (for web/mobile frontend)."""
    result = await ai_router.search(body)
    return APIResponse(success=True, data=result.model_dump())


@app.post("/api/documents/request")
async def api_request_document(body: DocumentRequestPayload):
    """Request a document; sends an SMS confirmation."""
    doc = await ai_router.get_document(body.doc_id)
    title = doc.title if doc else body.doc_id
    send_notification(
        phone_number=body.phone_number,
        notification_type=body.notification_type,
        context={"title": title, "doc_id": body.doc_id},
        language=body.language,
    )
    return APIResponse(
        success=True,
        message=f"Document '{title}' requested. SMS notification sent.",
    )


# =====================================================================
# Health & Admin
# =====================================================================

@app.get("/health")
async def health():
    ai_status = await ai_router.health()
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "ai_service": ai_status,
        "active_sessions": session_manager.active_count(),
    }


@app.get("/admin/sessions")
async def admin_sessions():
    """Return count of active USSD sessions (for monitoring)."""
    return APIResponse(
        success=True,
        data={"active_sessions": session_manager.active_count()},
    )
