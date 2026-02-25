"""
ArchiveAI – Voice Handler

Handles Africa's Talking voice callbacks:
  • Incoming calls → play welcome message
  • DTMF input → navigate voice menu
  • Record caller's voice query → forward recording URL to AI transcription
  • Callback with recording URL → store and transcribe

Africa's Talking voice API uses XML responses to control the call flow.
"""

from __future__ import annotations

import logging
from typing import Optional
from xml.etree.ElementTree import Element, SubElement, tostring

from app.config import settings
from app.models.models import VoiceCallback, VoiceRecording
from app.services.ai_service import ai_router

logger = logging.getLogger(__name__)

# In-memory store for voice recordings (swap for DB in production)
_recordings: dict[str, VoiceRecording] = {}


# ── XML response helpers ─────────────────────────────────────────────

def _xml_response(*elements: Element) -> str:
    """Wrap child elements in a <Response> root and serialise to XML string."""
    root = Element("Response")
    for el in elements:
        root.append(el)
    return tostring(root, encoding="unicode")


def _say(text: str) -> Element:
    el = Element("Say")
    el.text = text
    return el


def _get_digits(say_text: str, finish_on_key: str = "#", timeout: int = 30, num_digits: int = 1) -> Element:
    el = Element("GetDigits")
    el.set("finishOnKey", finish_on_key)
    el.set("timeout", str(timeout))
    el.set("numDigits", str(num_digits))
    say = SubElement(el, "Say")
    say.text = say_text
    return el


def _record(
    say_text: str,
    max_length: int = 30,
    finish_on_key: str = "#",
    trim_silence: bool = True,
    play_beep: bool = True,
) -> Element:
    el = Element("Record")
    el.set("maxLength", str(max_length))
    el.set("finishOnKey", finish_on_key)
    el.set("trimSilence", str(trim_silence).lower())
    el.set("playBeep", str(play_beep).lower())
    say = SubElement(el, "Say")
    say.text = say_text
    return el


def _play(url: str) -> Element:
    el = Element("Play")
    el.set("url", url)
    return el


def _reject() -> Element:
    return Element("Reject")


# ── Main voice callback handler ─────────────────────────────────────

async def handle_voice_callback(callback: VoiceCallback) -> str:
    """
    Process a voice callback from Africa's Talking.

    Returns an XML string that controls call flow.
    """
    logger.info(
        "Voice callback: session=%s caller=%s active=%s dtmf=%s recording=%s",
        callback.sessionId,
        callback.callerNumber,
        callback.isActive,
        callback.dtmfDigits,
        callback.recordingUrl,
    )

    # ── Call ended ───────────────────────────────────────────────────
    if callback.isActive == "0":
        logger.info("Call ended: session=%s", callback.sessionId)
        return _xml_response(_say("Thank you for calling ArchiveAI. Goodbye."))

    # ── Recording received ───────────────────────────────────────────
    if callback.recordingUrl:
        return await _handle_recording(callback)

    # ── DTMF digit received ──────────────────────────────────────────
    if callback.dtmfDigits:
        return _handle_dtmf(callback)

    # ── New incoming call → welcome menu ─────────────────────────────
    return _welcome_menu()


def _welcome_menu() -> str:
    """Return XML for the voice welcome menu."""
    prompt = (
        "Welcome to ArchiveAI, the intelligent archive search service. "
        "Press 1 to search the archive by voice. "
        "Press 2 to hear about our service. "
        "Press 0 to hang up."
    )
    return _xml_response(
        _get_digits(prompt, num_digits=1, timeout=10),
        _say("We did not receive any input. Goodbye."),
    )


def _handle_dtmf(callback: VoiceCallback) -> str:
    """Route DTMF (keypad) input."""
    digit = (callback.dtmfDigits or "").strip()

    if digit == "1":
        # Record a voice query
        return _xml_response(
            _record(
                "Please describe what you are looking for after the beep. "
                "Press hash when you are done.",
                max_length=30,
            ),
        )
    elif digit == "2":
        info = (
            "ArchiveAI helps you search historical documents from African "
            "libraries and archives. You can search by voice or by "
            "dialling our USSD code. Press 1 to search now, or 0 to exit."
        )
        return _xml_response(
            _get_digits(info, num_digits=1, timeout=10),
            _say("Goodbye."),
        )
    elif digit == "0":
        return _xml_response(_say("Thank you for calling. Goodbye."))
    else:
        return _welcome_menu()


async def _handle_recording(callback: VoiceCallback) -> str:
    """Store the recording and trigger transcription."""
    recording = VoiceRecording(
        session_id=callback.sessionId,
        phone_number=callback.callerNumber,
        recording_url=callback.recordingUrl,
        duration_seconds=(
            int(callback.durationInSeconds)
            if callback.durationInSeconds
            else None
        ),
    )
    _recordings[callback.sessionId] = recording
    logger.info("Stored recording for session %s: %s", callback.sessionId, callback.recordingUrl)

    # Attempt transcription via AI service
    transcription = await ai_router.transcribe(callback.recordingUrl)
    if transcription:
        recording.transcription = transcription
        return _xml_response(
            _say(f"We heard: {transcription}. We will send your results via SMS. Goodbye."),
        )

    return _xml_response(
        _say("We received your voice query and will process it shortly. "
             "You will receive results via SMS. Goodbye."),
    )


# ── Utility ──────────────────────────────────────────────────────────

def get_recording(session_id: str) -> Optional[VoiceRecording]:
    """Retrieve a stored voice recording by call session ID."""
    return _recordings.get(session_id)
