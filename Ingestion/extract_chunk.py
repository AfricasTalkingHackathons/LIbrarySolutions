"""
=============================================================
 Smart Archive Search Engine
 Module: Extract → Metadata → Chunk
 Handles: PDF, TXT, Markdown
 Author:  Your Team
=============================================================

 OUTPUT FORMAT
 Each processed document produces a list of chunk dicts:
 {
   "chunk_id":     "abc123_0001",
   "chunk_index":  1,
   "total_chunks": 42,
   "text":         "…chunk content…",
   "metadata": {
       "title":          "Introduction to Thermodynamics",
       "author":         "John Doe",
       "year":           "2021",
       "subject":        "Physics",
       "doc_type":       "Past Paper",
       "page_count":     12,
       "tags":           ["thermodynamics", "heat", "energy"],
       "source_file":    "thermo_2021.pdf",
       "source_path":    "/archive/past_papers/thermo_2021.pdf",
       "file_size_kb":   340.5,
       "file_hash":      "d41d8cd98f00b204…",
       "ingested_at":    "2024-01-01T10:00:00Z",
       "language":       "en",

       // ── Library location fields (new) ──
       "isbn":           "978-3-16-148410-0",
       "accession_no":   "ACC-2024-00123",
       "library_name":   "Main Campus Library",
       "shelf_number":   "SH-B4",
       "floor":          "2nd Floor",
       "room":           "Science Wing",
       "section":        "Physics",
       "availability":   "available",   // or "checked_out"
   }
 }
"""

import os
import re
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

import fitz                          #   — pip install PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter  # pip install langchain-text-splitters

# ──────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────
# CONFIGURATION  — tweak these to suit your archive
# ──────────────────────────────────────────────────────────

CHUNK_SIZE    = 512   # characters per chunk  (~100 words)
CHUNK_OVERLAP = 64    # overlap between chunks (prevents cut sentences)
MIN_CHUNK_LEN = 40    # discard chunks shorter than this (noise / headers)

# Map subfolder names → human-readable document type labels
DOC_TYPE_MAP = {
    "books":       "Book",
    "past_papers": "Past Paper",
    "oer":         "Open Educational Resource",
    "journals":    "Journal Article",
    "general":     "General",
}

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


# ══════════════════════════════════════════════════════════
# STEP 1 — EXTRACT
# ══════════════════════════════════════════════════════════

def extract_text_from_pdf(file_path: Path) -> tuple[str, int]:
    """
    Extract raw text from a PDF, page by page.

    Returns
    -------
    text       : full extracted text with page markers
    page_count : number of pages in the document
    """
    pages = []
    page_count = 0

    try:
        doc = fitz.open(str(file_path))
        page_count = len(doc)

        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")     # "text" = plain text layout

            # Clean up excessive whitespace within a page
            page_text = re.sub(r'\n{3,}', '\n\n', page_text).strip()

            if page_text:
                pages.append(f"[Page {page_num}]\n{page_text}")

        doc.close()
        log.info(f"    PDF extracted: {page_count} pages, {sum(len(p) for p in pages)} chars")

    except Exception as e:
        log.warning(f"    ⚠ PDF extraction failed for {file_path.name}: {e}")

    return "\n\n".join(pages), page_count


def extract_text_from_txt(file_path: Path) -> tuple[str, int]:
    """
    Read a plain text or Markdown file.

    Returns
    -------
    text       : file content
    page_count : estimated pages (every ~3000 chars ≈ 1 page)
    """
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")

        # For Markdown: strip common syntax so chunks are cleaner
        if file_path.suffix.lower() == ".md":
            text = _clean_markdown(text)

        page_count = max(1, len(text) // 3000)   # rough estimate
        log.info(f"    TXT extracted: ~{page_count} pages, {len(text)} chars")
        return text, page_count

    except Exception as e:
        log.warning(f"    ⚠ Text extraction failed for {file_path.name}: {e}")
        return "", 0


def _clean_markdown(text: str) -> str:
    """Strip Markdown syntax for cleaner chunking."""
    text = re.sub(r'#{1,6}\s*',      '',   text)   # headings
    text = re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', text)   # bold/italic
    text = re.sub(r'`{1,3}[^`]*`{1,3}',   '',   text)   # inline code
    text = re.sub(r'!\[.*?\]\(.*?\)',      '',   text)   # images
    text = re.sub(r'\[(.+?)\]\(.+?\)',  r'\1', text)   # links → text
    text = re.sub(r'^\s*[-*+]\s+',       '',   text, flags=re.MULTILINE)  # bullets
    text = re.sub(r'\n{3,}',          '\n\n', text)   # excessive newlines
    return text.strip()


def extract(file_path: Path) -> tuple[str, int]:
    """
    Route a file to the correct extractor.

    Returns (text, page_count)
    """
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".txt", ".md"):
        return extract_text_from_txt(file_path)
    else:
        log.warning(f"    Unsupported file type: {ext}")
        return "", 0


# ══════════════════════════════════════════════════════════
# STEP 2 — METADATA
# ══════════════════════════════════════════════════════════

def build_metadata(
    file_path:    Path,
    doc_type:     str,
    page_count:   int,
    text:         str,
    # ── Content fields (override auto-inference) ──────────
    author:       Optional[str] = None,
    year:         Optional[str] = None,
    subject:      Optional[str] = None,
    language:     Optional[str] = "en",
    tags:         Optional[list] = None,
    # ── Library location fields (from catalogue) ──────────
    isbn:         Optional[str] = None,
    accession_no: Optional[str] = None,
    library_name: Optional[str] = None,
    shelf_number: Optional[str] = None,
    floor:        Optional[str] = None,
    room:         Optional[str] = None,
    section:      Optional[str] = None,
    availability: Optional[str] = "available",
) -> dict:
    """
    Build a rich metadata dictionary for a document.

    Auto-infers what it can (title, year, subject, tags) from the file.
    Library location fields (isbn, shelf, floor, etc.) should be passed
    in from the catalogue — they default to None if not provided.
    """
    stat = file_path.stat()

    return {
        # ── Core identification ──────────────────────────
        "title":         _infer_title(file_path),
        "author":        author or "Unknown",
        "year":          year or _infer_year(file_path.stem),
        "subject":       subject or _infer_subject(file_path, doc_type),
        "doc_type":      doc_type,
        "language":      language,
        "tags":          tags or _extract_tags(text),

        # ── Document stats ───────────────────────────────
        "page_count":    page_count,
        "char_count":    len(text),

        # ── Library location fields ───────────────────────
        "isbn":          isbn,
        "accession_no":  accession_no,
        "library_name":  library_name,
        "shelf_number":  shelf_number,
        "floor":         floor,
        "room":          room,
        "section":       section,
        "availability":  availability,   # "available" | "checked_out"

        # ── Source traceability ──────────────────────────
        "source_file":   file_path.name,
        "source_path":   str(file_path.resolve()),
        "file_size_kb":  round(stat.st_size / 1024, 2),
        "file_hash":     _hash_file(file_path),

        # ── Ingestion tracking ───────────────────────────
        "ingested_at":   datetime.utcnow().isoformat() + "Z",
    }


# ── Metadata helper functions ──────────────────────────────

def _infer_title(file_path: Path) -> str:
    """Turn filename into a readable title."""
    name = file_path.stem
    name = re.sub(r'[_\-]+', ' ', name)        # underscores/dashes → spaces
    name = re.sub(r'\b(\d{4})\b', '', name)    # strip year numbers
    name = re.sub(r'\s+', ' ', name).strip()
    return name.title() or "Untitled"


def _infer_year(stem: str) -> Optional[str]:
    """Extract a 4-digit year from the filename stem."""
    match = re.search(r'\b(19|20)\d{2}\b', stem)
    return match.group(0) if match else None


def _infer_subject(file_path: Path, doc_type: str) -> str:
    """
    Guess subject from the folder structure.
    e.g.  past_papers/physics/paper1.pdf  →  "Physics"
    """
    parts = file_path.parts

    # Walk up parent folders for a meaningful name
    # Skip the root archive_data folder and the doc_type folder
    for part in reversed(parts[:-1]):
        if part.lower() not in DOC_TYPE_MAP and part != "archive_data":
            return part.replace("_", " ").title()

    return doc_type   # fallback


def _extract_tags(text: str, max_tags: int = 10) -> list[str]:
    """
    Extract candidate keyword tags from document text.

    Simple frequency-based approach:
    - Tokenise into lowercase words
    - Remove stopwords
    - Return the most frequent meaningful words as tags
    """
    STOPWORDS = {
        "the","a","an","and","or","but","in","on","at","to","for",
        "of","with","by","from","as","is","was","are","were","be",
        "been","being","have","has","had","do","does","did","will",
        "would","could","should","may","might","this","that","these",
        "those","it","its","we","our","you","your","they","their",
        "he","she","his","her","i","me","my","not","no","nor",
        "so","yet","both","also","more","other","such","than","too",
        "very","just","page","figure","table","section","chapter",
        "university","college","department","course","module",
    }

    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    freq  = {}
    for w in words:
        if w not in STOPWORDS:
            freq[w] = freq.get(w, 0) + 1

    # Sort by frequency, return top N
    sorted_words = sorted(freq, key=freq.get, reverse=True)
    return sorted_words[:max_tags]


def _hash_file(file_path: Path) -> str:
    """MD5 hash of file contents — used to detect duplicate files."""
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


# ══════════════════════════════════════════════════════════
# STEP 3 — CHUNK
# ══════════════════════════════════════════════════════════

def chunk_document(text: str, metadata: dict) -> list[dict]:
    """
    Split document text into overlapping chunks ready for embedding.

    Chunking strategy — RecursiveCharacterTextSplitter:
    Tries to split on:  paragraph → sentence → word → character
    This preserves semantic meaning as much as possible.

    Each chunk carries:
    - Its own text
    - A unique chunk_id  (file_hash + position index)
    - Its position within the document (chunk_index / total_chunks)
    - Full document metadata (so search results are always traceable)
    """
    if not text.strip():
        log.warning("    ⚠ Empty text — no chunks created")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    raw_chunks = splitter.split_text(text)
    chunks     = []

    for idx, raw in enumerate(raw_chunks):
        raw = raw.strip()

        # Drop chunks that are too short to be meaningful
        if len(raw) < MIN_CHUNK_LEN:
            continue

        chunk_id = f"{metadata['file_hash']}_{idx:04d}"

        chunks.append({
            "chunk_id":     chunk_id,
            "chunk_index":  idx,
            "total_chunks": len(raw_chunks),
            "text":         raw,
            "metadata":     metadata,
        })

    log.info(f"    Chunked → {len(chunks)} chunks  "
             f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


# ══════════════════════════════════════════════════════════
# ORCHESTRATOR — process one file end-to-end
# ══════════════════════════════════════════════════════════

def process_file(
    file_path:    Path,
    doc_type:     str,
    # Content overrides
    author:       Optional[str] = None,
    year:         Optional[str] = None,
    subject:      Optional[str] = None,
    language:     Optional[str] = "en",
    tags:         Optional[list] = None,
    # Library location fields
    isbn:         Optional[str] = None,
    accession_no: Optional[str] = None,
    library_name: Optional[str] = None,
    shelf_number: Optional[str] = None,
    floor:        Optional[str] = None,
    room:         Optional[str] = None,
    section:      Optional[str] = None,
    availability: Optional[str] = "available",
) -> list[dict]:
    """
    Run a single file through the full Extract → Metadata → Chunk pipeline.
    Library location fields flow through to every chunk's metadata.
    Returns a list of chunk dicts ready to be handed to the embedding step.
    """
    log.info(f"  📄 Processing: {file_path.name}")

    # ── Step 1: Extract ──────────────────────────────────
    text, page_count = extract(file_path)

    if not text.strip():
        log.warning(f"  ⚠ No text extracted from {file_path.name} — skipping")
        return []

    # ── Step 2: Metadata ─────────────────────────────────
    metadata = build_metadata(
        file_path=file_path,
        doc_type=doc_type,
        page_count=page_count,
        text=text,
        author=author,
        year=year,
        subject=subject,
        language=language,
        tags=tags,
        isbn=isbn,
        accession_no=accession_no,
        library_name=library_name,
        shelf_number=shelf_number,
        floor=floor,
        room=room,
        section=section,
        availability=availability,
    )

    # ── Step 3: Chunk ────────────────────────────────────
    chunks = chunk_document(text, metadata)

    return chunks


def process_directory(data_dir: str, catalogue_path: Optional[str] = None) -> list[dict]:
    """
    Walk the archive_data/ folder and process all supported files.
    If a catalogue JSON is provided, library location fields are merged
    into each document's metadata automatically.

    Expected structure:
        archive_data/
        ├── books/
        ├── past_papers/
        ├── oer/
        ├── journals/
        └── general/
    """
    data_path   = Path(data_dir)
    all_chunks  = []
    seen_hashes = set()

    if not data_path.exists():
        log.error(f"Directory not found: {data_dir}")
        return []

    # ── Load catalogue lookup if provided ────────────────
    catalogue = {}
    if catalogue_path and Path(catalogue_path).exists():
        catalogue = _load_catalogue(catalogue_path)
        log.info(f"📚 Catalogue loaded: {len(catalogue)} entries")

    for folder in sorted(data_path.iterdir()):
        if not folder.is_dir():
            continue

        doc_type = DOC_TYPE_MAP.get(folder.name.lower(), "General")
        log.info(f"\n📁 [{doc_type}] → {folder.name}/")

        for file_path in sorted(folder.rglob("*")):
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            file_hash = _hash_file(file_path)
            if file_hash in seen_hashes:
                log.info(f"  ⏭  Duplicate file skipped: {file_path.name}")
                continue
            seen_hashes.add(file_hash)

            # Look up catalogue entry by filename (stem) or accession_no
            cat = catalogue.get(file_path.stem, {})

            chunks = process_file(
                file_path=file_path,
                doc_type=doc_type,
                author=cat.get("author"),
                year=cat.get("year"),
                subject=cat.get("subject"),
                language=cat.get("language", "en"),
                tags=cat.get("tags"),
                isbn=cat.get("isbn"),
                accession_no=cat.get("accession_no"),
                library_name=cat.get("library_name"),
                shelf_number=cat.get("shelf_number"),
                floor=cat.get("floor"),
                room=cat.get("room"),
                section=cat.get("section"),
                availability=cat.get("availability", "available"),
            )
            all_chunks.extend(chunks)

    log.info(f"""
══════════════════════════════════════════
 Extraction & Chunking Complete
 Total chunks produced : {len(all_chunks)}
 Unique files processed: {len(seen_hashes)}
══════════════════════════════════════════""")

    return all_chunks


def _load_catalogue(catalogue_path: str) -> dict:
    """
    Load the library catalogue JSON.
    Returns a dict keyed by filename stem for fast lookup.
    e.g.  { "thermo_2021": { "isbn": "...", "shelf_number": "SH-B4", ... } }
    """
    with open(catalogue_path, encoding="utf-8") as f:
        entries = json.load(f)

    # Support both list format and dict format
    if isinstance(entries, list):
        return {e.get("filename_stem", e.get("title", "")): e for e in entries}
    return entries


# ══════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    # ── Process the whole archive ─────────────────────────
    # Pass catalogue_path if you have one — otherwise library fields will be None
    chunks = process_directory(
        data_dir="./archive_data",
        catalogue_path="./catalogue.json",   # optional — remove if not using
    )

    # ── Save output for inspection / handoff to teammate ──
    output_path = Path("./chunks_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    log.info(f"✅ Chunks saved → {output_path}  ({len(chunks)} total)")

    # ── Preview first 2 chunks ───────────────────────────
    print("\n── SAMPLE CHUNK OUTPUT ──────────────────────────────")
    for chunk in chunks[:2]:
        print(json.dumps(chunk, indent=2, ensure_ascii=False))
        print()