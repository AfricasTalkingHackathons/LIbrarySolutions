"""
=============================================================
 Smart Archive Search Engine
 Module: Library Catalogue Manager
 
 Manages the standalone catalogue of all physical/digital
 library resources — books, past papers, OERs, journals.

 Tracks:
   - ISBN / Accession Number
   - Shelf Number
   - Physical Location (floor, room, section)
   - Availability Status

 Usage:
   python catalogue.py                  # view all entries
   python catalogue.py --add            # add a new entry interactively
   python catalogue.py --update ACC001  # update an entry
   python catalogue.py --search physics # search the catalogue
   python catalogue.py --export         # export to CSV
=============================================================
"""

import json
import csv
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

CATALOGUE_FILE = "./catalogue.json"


# ══════════════════════════════════════════════════════════
# DATA MODEL
# ══════════════════════════════════════════════════════════

def make_entry(
    filename_stem: str,
    title:         str,
    doc_type:      str,
    # ── Content fields ────────────────────────────────────
    author:        Optional[str] = None,
    year:          Optional[str] = None,
    subject:       Optional[str] = None,
    language:      str = "en",
    tags:          Optional[list] = None,
    # ── Library identification ────────────────────────────
    isbn:          Optional[str] = None,
    accession_no:  Optional[str] = None,
    # ── Physical location ─────────────────────────────────
    library_name:  Optional[str] = None,
    shelf_number:  Optional[str] = None,
    floor:         Optional[str] = None,
    room:          Optional[str] = None,
    section:       Optional[str] = None,
    # ── Status ────────────────────────────────────────────
    availability:  str = "available",   # "available" | "checked_out"
    checked_out_by: Optional[str] = None,
    due_date:      Optional[str] = None,
) -> dict:
    """
    Create a validated catalogue entry dict.

    filename_stem must match the actual file on disk (without extension)
    so the ingestion pipeline can look it up by name.
    """
    if availability not in ("available", "checked_out"):
        raise ValueError("availability must be 'available' or 'checked_out'")

    return {
        # ── Linkage to file system ─────────────────────────
        "filename_stem":  filename_stem,     # e.g. "thermo_2021"  (no .pdf)
        "title":          title,
        "doc_type":       doc_type,

        # ── Content ───────────────────────────────────────
        "author":         author,
        "year":           str(year) if year else None,
        "subject":        subject,
        "language":       language,
        "tags":           tags or [],

        # ── Library identification ─────────────────────────
        "isbn":           isbn,
        "accession_no":   accession_no or _generate_accession(),

        # ── Physical location ──────────────────────────────
        "library_name":   library_name,
        "shelf_number":   shelf_number,       # e.g. "SH-B4"
        "floor":          floor,              # e.g. "2nd Floor"
        "room":           room,               # e.g. "Science Wing"
        "section":        section,            # e.g. "Physics"

        # ── Status ────────────────────────────────────────
        "availability":   availability,
        "checked_out_by": checked_out_by if availability == "checked_out" else None,
        "due_date":       due_date       if availability == "checked_out" else None,

        # ── Tracking ──────────────────────────────────────
        "added_at":       datetime.utcnow().isoformat() + "Z",
        "updated_at":     datetime.utcnow().isoformat() + "Z",
    }


def _generate_accession() -> str:
    """Auto-generate a unique accession number."""
    year = datetime.utcnow().year
    # Use a timestamp suffix for uniqueness in the hackathon context
    suffix = str(int(datetime.utcnow().timestamp()))[-5:]
    return f"ACC-{year}-{suffix}"


# ══════════════════════════════════════════════════════════
# PERSISTENCE
# ══════════════════════════════════════════════════════════

def load_catalogue() -> list[dict]:
    """Load the catalogue from JSON, return empty list if not found."""
    path = Path(CATALOGUE_FILE)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_catalogue(entries: list[dict]):
    """Write the catalogue to JSON."""
    with open(CATALOGUE_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"✅ Catalogue saved → {CATALOGUE_FILE}  ({len(entries)} entries)")


# ══════════════════════════════════════════════════════════
# CRUD OPERATIONS
# ══════════════════════════════════════════════════════════

def add_entry(entry: dict):
    """Add a new entry to the catalogue."""
    entries = load_catalogue()

    # Check for duplicate accession number
    existing = [e for e in entries if e.get("accession_no") == entry.get("accession_no")]
    if existing:
        print(f"⚠ Entry with accession_no '{entry['accession_no']}' already exists.")
        return

    entries.append(entry)
    save_catalogue(entries)
    print(f"✅ Added: [{entry['accession_no']}] {entry['title']}")


def update_entry(accession_no: str, updates: dict):
    """Update fields of an existing entry by accession number."""
    entries = load_catalogue()

    for entry in entries:
        if entry.get("accession_no") == accession_no:
            entry.update(updates)
            entry["updated_at"] = datetime.utcnow().isoformat() + "Z"
            save_catalogue(entries)
            print(f"✅ Updated: [{accession_no}]")
            return

    print(f"❌ Entry not found: {accession_no}")


def update_availability(accession_no: str, status: str,
                        checked_out_by: str = None, due_date: str = None):
    """
    Change availability status.
    status: "available" | "checked_out"
    """
    updates = {
        "availability":   status,
        "checked_out_by": checked_out_by if status == "checked_out" else None,
        "due_date":       due_date       if status == "checked_out" else None,
    }
    update_entry(accession_no, updates)


def search_catalogue(query: str) -> list[dict]:
    """
    Simple keyword search across title, author, subject, tags, location fields.
    """
    query_lower = query.lower()
    entries     = load_catalogue()
    results     = []

    for entry in entries:
        searchable = " ".join(str(v) for v in [
            entry.get("title", ""),
            entry.get("author", ""),
            entry.get("subject", ""),
            entry.get("section", ""),
            entry.get("shelf_number", ""),
            entry.get("library_name", ""),
            " ".join(entry.get("tags", [])),
        ]).lower()

        if query_lower in searchable:
            results.append(entry)

    return results


def get_by_accession(accession_no: str) -> Optional[dict]:
    """Fetch a single entry by its accession number."""
    for entry in load_catalogue():
        if entry.get("accession_no") == accession_no:
            return entry
    return None


# ══════════════════════════════════════════════════════════
# DISPLAY
# ══════════════════════════════════════════════════════════

def print_entry(entry: dict):
    """Pretty-print a single catalogue entry."""
    avail_icon = "✅" if entry.get("availability") == "available" else "🔴"
    print(f"""
  ┌─────────────────────────────────────────────
  │ {entry.get('title', 'Untitled')}
  │ Type       : {entry.get('doc_type')}
  │ Author     : {entry.get('author', 'Unknown')}
  │ Year       : {entry.get('year', 'N/A')}
  │ Subject    : {entry.get('subject', 'N/A')}
  ├─────────────────────────────────────────────
  │ ISBN       : {entry.get('isbn', 'N/A')}
  │ Accession  : {entry.get('accession_no')}
  ├─────────────────────────────────────────────
  │ Library    : {entry.get('library_name', 'N/A')}
  │ Shelf      : {entry.get('shelf_number', 'N/A')}
  │ Floor      : {entry.get('floor', 'N/A')}
  │ Room       : {entry.get('room', 'N/A')}
  │ Section    : {entry.get('section', 'N/A')}
  ├─────────────────────────────────────────────
  │ Status     : {avail_icon} {entry.get('availability', 'unknown').upper()}""")

    if entry.get("availability") == "checked_out":
        print(f"  │ Checked by : {entry.get('checked_out_by', 'N/A')}")
        print(f"  │ Due date   : {entry.get('due_date', 'N/A')}")

    print(f"  │ Tags       : {', '.join(entry.get('tags', []))}")
    print(f"  └─────────────────────────────────────────────")


def print_catalogue(entries: list[dict]):
    """Print all catalogue entries."""
    if not entries:
        print("📭 Catalogue is empty.")
        return
    print(f"\n📚 Library Catalogue — {len(entries)} item(s)\n")
    for entry in entries:
        print_entry(entry)


# ══════════════════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════════════════

def export_to_csv(output_path: str = "./catalogue_export.csv"):
    """Export catalogue to CSV for spreadsheet use."""
    entries = load_catalogue()
    if not entries:
        print("Nothing to export.")
        return

    fields = [
        "accession_no", "isbn", "filename_stem", "title", "doc_type",
        "author", "year", "subject", "language", "tags",
        "library_name", "shelf_number", "floor", "room", "section",
        "availability", "checked_out_by", "due_date",
        "added_at", "updated_at",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            row = dict(entry)
            row["tags"] = ", ".join(row.get("tags", []))
            writer.writerow(row)

    print(f"✅ Exported {len(entries)} entries → {output_path}")


# ══════════════════════════════════════════════════════════
# — run once to populate a demo catalogue
# ══════════════════════════════════════════════════════════

def seed_sample_catalogue():
    """Create a sample catalogue.json with realistic entries for demo purposes."""
    samples = [
        make_entry(
            filename_stem="introduction_to_algorithms",
            title="Introduction to Algorithms",
            doc_type="Book",
            author="Cormen, Leiserson, Rivest, Stein",
            year="2009",
            subject="Computer Science",
            isbn="978-0-262-03384-8",
            accession_no="ACC-2024-00001",
            library_name="Main Campus Library",
            shelf_number="SH-CS3",
            floor="3rd Floor",
            room="Computing Wing",
            section="Algorithms & Data Structures",
            availability="available",
            tags=["algorithms", "data structures", "sorting", "graphs"],
        ),
        make_entry(
            filename_stem="physics_past_paper_2022",
            title="Physics Past Paper 2022",
            doc_type="Past Paper",
            subject="Physics",
            year="2022",
            accession_no="ACC-2024-00002",
            library_name="Main Campus Library",
            shelf_number="SH-PP1",
            floor="1st Floor",
            room="Exam Papers Room",
            section="Physics",
            availability="available",
            tags=["physics", "mechanics", "thermodynamics", "waves"],
        ),
        make_entry(
            filename_stem="open_textbook_calculus",
            title="Open Textbook: Calculus",
            doc_type="Open Educational Resource",
            author="OpenStax",
            year="2021",
            isbn="978-1-947172-13-5",
            accession_no="ACC-2024-00003",
            library_name="Digital Resource Centre",
            shelf_number="DIGITAL",
            floor="N/A",
            room="Online Repository",
            section="Mathematics",
            availability="available",
            tags=["calculus", "derivatives", "integrals", "limits"],
        ),
        make_entry(
            filename_stem="machine_learning_book",
            title="Pattern Recognition and Machine Learning",
            doc_type="Book",
            author="Christopher Bishop",
            year="2006",
            isbn="978-0-387-31073-2",
            accession_no="ACC-2024-00004",
            library_name="Main Campus Library",
            shelf_number="SH-AI2",
            floor="2nd Floor",
            room="Science Wing",
            section="Artificial Intelligence",
            availability="checked_out",
            checked_out_by="Student ID: S12345",
            due_date="2024-02-15",
            tags=["machine learning", "neural networks", "bayesian", "classification"],
        ),
    ]

    save_catalogue(samples)
    print(f"🌱 Seeded {len(samples)} sample catalogue entries.")


# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Library Catalogue Manager")
    parser.add_argument("--list",   action="store_true", help="List all entries")
    parser.add_argument("--search", type=str,            help="Search by keyword")
    parser.add_argument("--get",    type=str,            help="Get entry by accession no.")
    parser.add_argument("--export", action="store_true", help="Export to CSV")
    parser.add_argument("--seed",   action="store_true", help="Seed sample data")
    parser.add_argument("--checkin",  type=str,          help="Mark item as available (accession no.)")
    parser.add_argument("--checkout", type=str,          help="Mark item as checked out (accession no.)")
    parser.add_argument("--by",     type=str,            help="Student/borrower ID (for --checkout)")
    parser.add_argument("--due",    type=str,            help="Due date YYYY-MM-DD (for --checkout)")

    args = parser.parse_args()

    if args.seed:
        seed_sample_catalogue()

    elif args.list:
        print_catalogue(load_catalogue())

    elif args.search:
        results = search_catalogue(args.search)
        print(f"\n🔍 Search: '{args.search}' → {len(results)} result(s)")
        print_catalogue(results)

    elif args.get:
        entry = get_by_accession(args.get)
        if entry:
            print_entry(entry)
        else:
            print(f"❌ Not found: {args.get}")

    elif args.export:
        export_to_csv()

    elif args.checkin:
        update_availability(args.checkin, "available")
        print(f"✅ {args.checkin} marked as AVAILABLE")

    elif args.checkout:
        update_availability(
            args.checkout, "checked_out",
            checked_out_by=args.by,
            due_date=args.due,
        )
        print(f"🔴 {args.checkout} marked as CHECKED OUT")

    else:
        # Default: show catalogue + usage hint
        print_catalogue(load_catalogue())
        print("\nTip: run  python catalogue.py --seed  to load sample data")
        print("     run  python catalogue.py --help  for all options")