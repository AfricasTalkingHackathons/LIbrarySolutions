"""
ArchiveAI – Application entry point.

Run with:
    uvicorn main:app --reload
or:
    python main.py
"""

import uvicorn

from app.api.api import app  # noqa: F401 – re-export for uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
