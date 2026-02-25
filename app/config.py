"""
ArchiveAI Configuration
Loads environment variables and provides centralized config for AT credentials,
database, AI service, and application settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application-wide settings loaded from environment variables."""

    # ── Africa's Talking Credentials ─────────────────────────────────
    AT_USERNAME: str = os.getenv("AT_USERNAME", "sandbox")
    AT_API_KEY: str = os.getenv("AT_API_KEY", "")
    AT_USSD_CODE: str = os.getenv("AT_USSD_CODE", "*384*1234#")
    AT_SHORTCODE: str = os.getenv("AT_SHORTCODE", "")  # SMS shortcode
    AT_VOICE_NUMBER: str = os.getenv("AT_VOICE_NUMBER", "")  # Voice phone number

    # ── AI / Search Service ──────────────────────────────────────────
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:8001")
    AI_SERVICE_TIMEOUT: int = int(os.getenv("AI_SERVICE_TIMEOUT", "30"))

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/archiveai"
    )

    # ── Session ──────────────────────────────────────────────────────
    SESSION_TTL_SECONDS: int = int(os.getenv("SESSION_TTL_SECONDS", "300"))  # 5 min

    # ── Application ──────────────────────────────────────────────────
    APP_NAME: str = "ArchiveAI"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ── Supported Languages ──────────────────────────────────────────
    SUPPORTED_LANGUAGES: dict = {
        "en": "English",
        "sw": "Swahili",
        "ki": "Kikuyu",
        "am": "Amharic",
    }
    DEFAULT_LANGUAGE: str = "en"


settings = Settings()
