"""
ArchiveAI – AI Service Router

Proxies requests to the AI / NLP micro-service that handles:
  • Semantic search (transformer-based embeddings)
  • OCR document lookup
  • Metadata extraction

When the AI service is unreachable, falls back to a local keyword
search over a built-in sample document catalogue.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx

from app.config import settings
from app.models.models import DocumentResult, SearchRequest, SearchResponse

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────
# Sample document catalogue (fallback when AI service is offline)
# ─────────────────────────────────────────────────────────────────────

_SAMPLE_DOCS: List[Dict[str, Any]] = [
    {
        "doc_id": "DOC001",
        "title": "The Kenya Land Commission Report (1933)",
        "snippet": "Comprehensive analysis of colonial-era land grievances, dispossession of native reserves, and recommendations for land redistribution in Kenya Colony.",
        "tags": ["kenya", "land", "colonial", "1933", "commission", "dispute", "grievance"],
        "language": "en",
    },
    {
        "doc_id": "DOC002",
        "title": "Crown Lands Ordinance (1915)",
        "snippet": "Legal framework establishing Crown ownership of all 'waste and unoccupied' land in British East Africa, displacing indigenous land rights.",
        "tags": ["kenya", "land", "colonial", "1915", "ordinance", "crown", "law", "british"],
        "language": "en",
    },
    {
        "doc_id": "DOC003",
        "title": "Devonshire White Paper (1923)",
        "snippet": "Declaration that Kenya is primarily African territory, resolving the conflict between European settler and Indian immigrant land claims.",
        "tags": ["kenya", "1923", "devonshire", "land", "colonial", "settlers", "african"],
        "language": "en",
    },
    {
        "doc_id": "DOC004",
        "title": "Mau Mau Detention Camps - Pipeline System (1954-1960)",
        "snippet": "Documentation of the British colonial screening and detention system used during the Kenya Emergency, including forced labor and rehabilitation camps.",
        "tags": ["mau mau", "detention", "kenya", "colonial", "emergency", "1954", "pipeline", "british"],
        "language": "en",
    },
    {
        "doc_id": "DOC005",
        "title": "Hola Massacre Report (1959)",
        "snippet": "Official inquiry into the beating deaths of 11 Mau Mau detainees at Hola detention camp, which accelerated the push for Kenyan independence.",
        "tags": ["hola", "massacre", "mau mau", "detention", "kenya", "1959", "independence"],
        "language": "en",
    },
    {
        "doc_id": "DOC006",
        "title": "Lancaster House Conference Records (1960-1963)",
        "snippet": "Transcripts of the constitutional conferences in London that negotiated the terms of Kenya's transition to self-governance and independence.",
        "tags": ["lancaster", "independence", "kenya", "1960", "constitution", "conference", "self-governance"],
        "language": "en",
    },
    {
        "doc_id": "DOC007",
        "title": "Kapenguria Six Trial Proceedings (1952-1953)",
        "snippet": "Court records from the trial of Jomo Kenyatta and five others charged with managing the Mau Mau movement, a pivotal moment in Kenya's independence struggle.",
        "tags": ["kapenguria", "kenyatta", "trial", "mau mau", "kenya", "1952", "independence"],
        "language": "en",
    },
    {
        "doc_id": "DOC008",
        "title": "Mombasa: Mji wa Kale - Historia ya Bandari",
        "snippet": "Historia ya kina ya mji wa Mombasa tangu karne ya 11, biashara ya Waarabu, na kuingia kwa Wareno katika pwani ya Afrika Mashariki.",
        "tags": ["mombasa", "historia", "pwani", "bandari", "swahili", "kenya", "biashara"],
        "language": "sw",
    },
    {
        "doc_id": "DOC009",
        "title": "Fort Jesus na Wareno (1593-1698)",
        "snippet": "Ujenzi wa ngome ya Fort Jesus na Wareno mwaka 1593, vita vya kutawala pwani ya Afrika Mashariki, na ushindi wa Waomani.",
        "tags": ["fort jesus", "mombasa", "wareno", "portuguese", "1593", "pwani", "ngome"],
        "language": "sw",
    },
    {
        "doc_id": "DOC010",
        "title": "Maji Maji Rebellion Records (1905-1907)",
        "snippet": "Primary sources documenting the uprising against German colonial rule in Tanganyika, the largest armed resistance in East African colonial history.",
        "tags": ["maji maji", "rebellion", "tanganyika", "german", "colonial", "1905", "tanzania", "resistance"],
        "language": "en",
    },
    {
        "doc_id": "DOC011",
        "title": "Swahili Coast Trade Routes (800-1500 AD)",
        "snippet": "Archaeological and documentary evidence of Indian Ocean trade networks connecting the Swahili coast with Arabia, Persia, India, and China.",
        "tags": ["swahili", "coast", "trade", "indian ocean", "arabia", "medieval", "archaeology"],
        "language": "en",
    },
    {
        "doc_id": "DOC012",
        "title": "Lalibela Rock-Hewn Churches Manuscript Collection",
        "snippet": "Catalogue of Ge'ez manuscripts preserved in the rock-hewn churches of Lalibela, Ethiopia, dating from the 12th to 18th centuries.",
        "tags": ["lalibela", "ethiopia", "church", "manuscript", "geez", "orthodox", "medieval"],
        "language": "en",
    },
    {
        "doc_id": "DOC013",
        "title": "Kikuyu Land Tenure Traditions",
        "snippet": "Ethnographic study of traditional Kikuyu land ownership systems including githaka (family land units) and the role of mbari (sub-clan) governance.",
        "tags": ["kikuyu", "land", "tenure", "tradition", "githaka", "mbari", "kenya", "indigenous"],
        "language": "en",
    },
    {
        "doc_id": "DOC014",
        "title": "Emergency Regulations - Kenya (1952)",
        "snippet": "Full text of the emergency powers declared by Governor Evelyn Baring on 20 October 1952, authorising detention without trial and military operations.",
        "tags": ["emergency", "kenya", "1952", "colonial", "mau mau", "detention", "baring", "regulations"],
        "language": "en",
    },
    {
        "doc_id": "DOC015",
        "title": "Vita vya Maji Maji (1905-1907)",
        "snippet": "Kumbukumbu za vita vya Maji Maji dhidi ya ukoloni wa Kijerumani huko Tanganyika. Maasi makubwa zaidi katika historia ya Afrika Mashariki.",
        "tags": ["maji maji", "vita", "tanganyika", "ukoloni", "kijerumani", "tanzania", "maasi"],
        "language": "sw",
    },
]


def _keyword_search(query: str, top_k: int = 5) -> List[DocumentResult]:
    """Simple keyword matching against the sample catalogue."""
    query_lower = query.lower()
    terms = query_lower.split()

    scored: List[tuple[float, Dict]] = []
    for doc in _SAMPLE_DOCS:
        score = 0.0
        searchable = f"{doc['title']} {doc['snippet']} {' '.join(doc['tags'])}".lower()
        for term in terms:
            if term in searchable:
                score += 1.0
            # Bonus for tag match
            for tag in doc["tags"]:
                if term in tag:
                    score += 0.5
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, doc in scored[:top_k]:
        normalized_score = min(score / max(len(terms), 1), 1.0)
        results.append(
            DocumentResult(
                doc_id=doc["doc_id"],
                title=doc["title"],
                snippet=doc["snippet"],
                score=round(normalized_score, 2),
                metadata={"language": doc["language"], "source": "local_catalogue"},
            )
        )
    return results


class AIServiceRouter:
    """Lightweight HTTP proxy to the AI search backend."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self._base_url = (base_url or settings.AI_SERVICE_URL).rstrip("/")
        self._timeout = timeout or settings.AI_SERVICE_TIMEOUT

    # ── Semantic Search ──────────────────────────────────────────────

    async def search(self, request: SearchRequest) -> SearchResponse:
        """
        Send a semantic-search query to the AI service and return
        parsed results.  Falls back to local keyword search if the
        AI service is unreachable.

        Endpoint: POST {AI_SERVICE_URL}/api/search
        """
        url = f"{self._base_url}/api/search"
        payload = request.model_dump()
        logger.info("AI search → %s  query=%r", url, request.query)

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return SearchResponse(**data)
        except Exception as exc:
            logger.warning("AI service unavailable (%s), using local fallback", exc)

        # ── Fallback: local keyword search ───────────────────────────
        results = _keyword_search(request.query, top_k=request.top_k)
        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
        )

    # ── Single Document Lookup ───────────────────────────────────────

    async def get_document(self, doc_id: str) -> Optional[DocumentResult]:
        """
        Fetch full document metadata by ID.

        Endpoint: GET {AI_SERVICE_URL}/api/documents/{doc_id}
        """
        url = f"{self._base_url}/api/documents/{doc_id}"
        logger.info("AI doc lookup → %s", url)

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                return DocumentResult(**resp.json())
        except Exception as exc:
            logger.error("Document lookup failed for %s: %s", doc_id, exc)
            return None

    # ── Voice Transcription ──────────────────────────────────────────

    async def transcribe(
        self,
        recording_url: str,
        language: str = "en",
    ) -> Optional[str]:
        """
        Send a voice recording URL to the AI service for transcription.

        Endpoint: POST {AI_SERVICE_URL}/api/transcribe
        """
        url = f"{self._base_url}/api/transcribe"
        payload = {"recording_url": recording_url, "language": language}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data.get("text")
        except Exception as exc:
            logger.error("Transcription failed: %s", exc)
            return None

    # ── Health Check ─────────────────────────────────────────────────

    async def health(self) -> Dict[str, Any]:
        """Ping the AI service health endpoint."""
        url = f"{self._base_url}/health"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(url)
                return resp.json()
        except Exception:
            return {"status": "unreachable"}


# Singleton
ai_router = AIServiceRouter()
