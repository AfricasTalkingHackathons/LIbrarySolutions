"""
ArchiveAI – USSD Flow Handler

Implements the full USSD menu tree for Africa's Talking gateway:

  *384*1234#
  ├─ 1. Select Language
  ├─ 2. Search Archive
  │     ├─ enter query → results list
  │     └─ select result → detail + request copy
  ├─ 3. My Requests
  └─ 0. Exit

The handler receives the cumulative `text` field from AT (values
separated by `*`) and walks the session state machine accordingly.
"""

from __future__ import annotations

import logging
from typing import List

from app.config import settings
from app.models.models import (
    SearchRequest,
    USSDRequest,
    USSDSession,
    USSDStage,
)
from app.services.ai_service import ai_router
from app.services.session_manager import session_manager

logger = logging.getLogger(__name__)

# ── Localised UI strings ────────────────────────────────────────────

STRINGS = {
    "en": {
        "welcome": (
            "Welcome to ArchiveAI\n"
            "1. Search Archive\n"
            "2. Change Language\n"
            "3. My Requests\n"
            "0. Exit"
        ),
        "language_select": (
            "Select language:\n"
            "1. English\n"
            "2. Swahili\n"
            "3. Kikuyu\n"
            "4. Amharic"
        ),
        "search_prompt": "Enter your search query:\ne.g. colonial land disputes 1920s Kenya",
        "searching": "Searching the archive, please wait...",
        "no_results": "No results found. Try a different query.\n0. Back to menu",
        "results_header": "Results:\n",
        "doc_detail": "Title: {title}\n{snippet}\n\n1. Request this document via SMS\n0. Back to results",
        "request_sent": "Your request has been submitted! You will receive an SMS when the document is ready.\n0. Back to menu",
        "my_requests": "Feature coming soon.\n0. Back to menu",
        "goodbye": "Thank you for using ArchiveAI. Goodbye!",
        "error": "Something went wrong. Please try again.\n0. Back to menu",
        "language_set": "Language updated to {lang}.\n0. Back to menu",
    },
    "sw": {
        "welcome": (
            "Karibu ArchiveAI\n"
            "1. Tafuta Kumbukumbu\n"
            "2. Badilisha Lugha\n"
            "3. Maombi Yangu\n"
            "0. Toka"
        ),
        "language_select": (
            "Chagua lugha:\n"
            "1. Kiingereza\n"
            "2. Kiswahili\n"
            "3. Kikuyu\n"
            "4. Kiamhara"
        ),
        "search_prompt": "Andika swali lako la utafutaji:\nmfano: migogoro ya ardhi 1920 Kenya",
        "searching": "Inatafuta kumbukumbu, subiri...",
        "no_results": "Hakuna matokeo. Jaribu swali lingine.\n0. Rudi kwenye menyu",
        "results_header": "Matokeo:\n",
        "doc_detail": "Kichwa: {title}\n{snippet}\n\n1. Omba hati hii kupitia SMS\n0. Rudi kwenye matokeo",
        "request_sent": "Ombi lako limetumwa! Utapokea SMS hati ikiwa tayari.\n0. Rudi kwenye menyu",
        "my_requests": "Kipengele kinakuja hivi karibuni.\n0. Rudi kwenye menyu",
        "goodbye": "Asante kwa kutumia ArchiveAI. Kwaheri!",
        "error": "Kuna tatizo. Tafadhali jaribu tena.\n0. Rudi kwenye menyu",
        "language_set": "Lugha imebadilishwa kuwa {lang}.\n0. Rudi kwenye menyu",
    },
}

# Fallback to English for unsupported languages
def _t(lang: str, key: str, **kwargs) -> str:
    table = STRINGS.get(lang, STRINGS["en"])
    template = table.get(key, STRINGS["en"].get(key, ""))
    return template.format(**kwargs) if kwargs else template


# Language-code map (option number → code)
LANG_MAP = {"1": "en", "2": "sw", "3": "ki", "4": "am"}


# ── Main USSD handler ───────────────────────────────────────────────

async def handle_ussd(request: USSDRequest) -> str:
    """
    Process a single USSD callback from Africa's Talking.

    Returns the response string. Prefix with:
      CON  – keep session open (more input expected)
      END  – terminate session after displaying message

    Africa's Talking `text` field: cumulative, split by `*`.
    Example:  "" → "1" → "1*colonial land" → "1*colonial land*2"
    """

    session = session_manager.get_or_create(
        session_id=request.sessionId,
        phone_number=request.phoneNumber,
    )

    # Parse the latest user input from the cumulative text
    parts: List[str] = [p for p in request.text.split("*") if p]
    user_input = parts[-1].strip() if parts else ""
    depth = len(parts)

    logger.info(
        "USSD sid=%s stage=%s depth=%d input=%r",
        session.session_id,
        session.stage.value,
        depth,
        user_input,
    )

    try:
        response = await _route(session, user_input, depth)
    except Exception as exc:
        logger.exception("USSD handler error: %s", exc)
        response = f"END {_t(session.language, 'error')}"

    session_manager.update(session)
    return response


async def _route(session: USSDSession, user_input: str, depth: int) -> str:
    """State-machine router."""

    lang = session.language

    # ── First interaction (empty text) ───────────────────────────────
    if depth == 0:
        session.stage = USSDStage.MAIN_MENU
        return f"CON {_t(lang, 'welcome')}"

    # ── Main menu selections ─────────────────────────────────────────
    if session.stage == USSDStage.MAIN_MENU:
        if user_input == "1":
            session.stage = USSDStage.SEARCH_INPUT
            return f"CON {_t(lang, 'search_prompt')}"
        elif user_input == "2":
            session.stage = USSDStage.LANGUAGE_SELECT
            return f"CON {_t(lang, 'language_select')}"
        elif user_input == "3":
            session.stage = USSDStage.MAIN_MENU
            return f"CON {_t(lang, 'my_requests')}"
        elif user_input == "0":
            session_manager.delete(session.session_id)
            return f"END {_t(lang, 'goodbye')}"
        else:
            return f"CON {_t(lang, 'welcome')}"

    # ── Language selection ────────────────────────────────────────────
    if session.stage == USSDStage.LANGUAGE_SELECT:
        new_lang = LANG_MAP.get(user_input, "en")
        session.language = new_lang
        lang = new_lang
        session.stage = USSDStage.MAIN_MENU
        lang_name = settings.SUPPORTED_LANGUAGES.get(new_lang, "English")
        return f"CON {_t(lang, 'language_set', lang=lang_name)}"

    # ── Search input ─────────────────────────────────────────────────
    if session.stage == USSDStage.SEARCH_INPUT:
        session.search_query = user_input
        search_req = SearchRequest(query=user_input, language=lang)
        search_resp = await ai_router.search(search_req)
        session.search_results = [r.model_dump() for r in search_resp.results]

        if not session.search_results:
            session.stage = USSDStage.MAIN_MENU
            return f"CON {_t(lang, 'no_results')}"

        session.stage = USSDStage.SEARCH_RESULTS
        menu = _t(lang, "results_header")
        for idx, doc in enumerate(session.search_results[:5], start=1):
            title = doc.get("title", "Untitled")[:40]
            menu += f"{idx}. {title}\n"
        menu += "0. Back"
        return f"CON {menu}"

    # ── Search results selection ─────────────────────────────────────
    if session.stage == USSDStage.SEARCH_RESULTS:
        if user_input == "0":
            session.stage = USSDStage.MAIN_MENU
            return f"CON {_t(lang, 'welcome')}"
        try:
            idx = int(user_input) - 1
            doc = session.search_results[idx]
        except (ValueError, IndexError):
            return f"CON {_t(lang, 'error')}"

        session.selected_doc_index = idx
        session.stage = USSDStage.DOCUMENT_DETAIL
        return f"CON {_t(lang, 'doc_detail', title=doc.get('title', ''), snippet=doc.get('snippet', '')[:120])}"

    # ── Document detail ──────────────────────────────────────────────
    if session.stage == USSDStage.DOCUMENT_DETAIL:
        if user_input == "1":
            # Request document → trigger SMS notification
            session.stage = USSDStage.MAIN_MENU
            doc = session.search_results[session.selected_doc_index or 0]
            session.extra["last_requested_doc_id"] = doc.get("doc_id")
            return f"CON {_t(lang, 'request_sent')}"
        elif user_input == "0":
            session.stage = USSDStage.SEARCH_RESULTS
            # Re-display results
            menu = _t(lang, "results_header")
            for i, d in enumerate(session.search_results[:5], start=1):
                menu += f"{i}. {d.get('title', 'Untitled')[:40]}\n"
            menu += "0. Back"
            return f"CON {menu}"

    # ── Fallback ─────────────────────────────────────────────────────
    if user_input == "0":
        session.stage = USSDStage.MAIN_MENU
        return f"CON {_t(lang, 'welcome')}"

    return f"CON {_t(lang, 'welcome')}"
