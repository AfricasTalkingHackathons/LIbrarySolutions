"""
ArchiveAI – SMS Service

Send and receive SMS via Africa's Talking.
Handles:
  • Inbound SMS → parse query → route to AI search → reply with results
  • Outbound notifications (document ready, reservation confirmations)
  • Delivery reports
"""

from __future__ import annotations

import logging
from typing import List, Optional

import africastalking

from app.config import settings
from app.models.models import (
    DocumentResult,
    InboundSMS,
    NotificationType,
    OutboundSMS,
    SearchRequest,
)
from app.services.ai_service import ai_router

logger = logging.getLogger(__name__)

# ── Initialise Africa's Talking SDK ─────────────────────────────────
africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
sms_client = africastalking.SMS


# ── Send SMS ─────────────────────────────────────────────────────────

def send_sms(recipients: List[str], message: str, sender: Optional[str] = None) -> dict:
    """
    Send an SMS to one or more recipients.

    Returns the Africa's Talking API response dict.
    """
    sender = sender or settings.AT_SHORTCODE or None
    try:
        kwargs = {"message": message, "recipients": recipients}
        if sender:
            kwargs["sender_id"] = sender
        response = sms_client.send(**kwargs)
        logger.info("SMS sent to %s: %s", recipients, response)
        return response
    except Exception as exc:
        logger.exception("Failed to send SMS: %s", exc)
        return {"error": str(exc)}


def send_notification(
    phone_number: str,
    notification_type: NotificationType,
    context: dict,
    language: str = "en",
) -> dict:
    """
    Send a templated notification SMS.

    `context` should contain keys relevant to the notification type,
    e.g. {"title": "Land Act 1921", "doc_id": "abc123"}.
    """
    message = _build_notification_message(notification_type, context, language)
    return send_sms([phone_number], message)


# ── Inbound SMS processing ──────────────────────────────────────────

async def handle_inbound_sms(sms: InboundSMS) -> dict:
    """
    Process an inbound SMS:
      1. Treat the body as a search query.
      2. Forward to the AI service.
      3. Reply with top results via SMS.
    """
    logger.info("Inbound SMS from %s: %s", sms.from_, sms.text)

    query_text = sms.text.strip()
    if not query_text:
        send_sms([sms.from_], "Welcome to ArchiveAI! Send a search query to find documents.")
        return {"status": "empty_query"}

    # Route to AI service
    search_req = SearchRequest(query=query_text, language="en")
    search_resp = await ai_router.search(search_req)

    if not search_resp.results:
        send_sms(
            [sms.from_],
            f"No results found for: \"{query_text}\". Try different keywords.",
        )
        return {"status": "no_results"}

    # Format top results
    reply = f"ArchiveAI results for \"{query_text}\":\n\n"
    for idx, doc in enumerate(search_resp.results[:3], start=1):
        reply += f"{idx}. {doc.title}\n   {doc.snippet[:80]}\n\n"
    reply += "Reply with the number to request a document."

    # Truncate to SMS limit (≈ 480 chars for 3-part SMS)
    if len(reply) > 480:
        reply = reply[:477] + "..."

    send_sms([sms.from_], reply)
    return {"status": "results_sent", "count": len(search_resp.results)}


# ── Delivery reports ─────────────────────────────────────────────────

def handle_delivery_report(report: dict) -> None:
    """Log delivery report from Africa's Talking callback."""
    logger.info(
        "SMS delivery: id=%s status=%s phone=%s",
        report.get("id"),
        report.get("status"),
        report.get("phoneNumber"),
    )


# ── Notification templates ───────────────────────────────────────────

def _build_notification_message(
    ntype: NotificationType,
    ctx: dict,
    lang: str,
) -> str:
    """Return a human-readable notification string."""
    templates = {
        "en": {
            NotificationType.DOCUMENT_READY: (
                "ArchiveAI: The document \"{title}\" is ready for pickup/download. "
                "Reference: {doc_id}"
            ),
            NotificationType.SEARCH_RESULT: (
                "ArchiveAI: We found {count} results for your query."
            ),
            NotificationType.RESERVATION_CONFIRM: (
                "ArchiveAI: Your reservation for \"{title}\" has been confirmed."
            ),
            NotificationType.REMINDER: (
                "ArchiveAI: Reminder – please collect your document \"{title}\"."
            ),
        },
        "sw": {
            NotificationType.DOCUMENT_READY: (
                "ArchiveAI: Hati \"{title}\" iko tayari. Rejea: {doc_id}"
            ),
            NotificationType.SEARCH_RESULT: (
                "ArchiveAI: Tumepata matokeo {count} kwa swali lako."
            ),
            NotificationType.RESERVATION_CONFIRM: (
                "ArchiveAI: Uhifadhi wako wa \"{title}\" umethibitishwa."
            ),
            NotificationType.REMINDER: (
                "ArchiveAI: Kumbusho – tafadhali chukua hati yako \"{title}\"."
            ),
        },
    }
    lang_templates = templates.get(lang, templates["en"])
    template = lang_templates.get(ntype, "ArchiveAI: You have a new notification.")
    try:
        return template.format(**ctx)
    except KeyError:
        return template
