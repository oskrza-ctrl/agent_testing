import re
from pathlib import Path
from typing import List, Dict


# Folders with one big accumulative file — split by entry separator
ACCUMULATIVE_FOLDERS = {"Ideas", "Tasks", "Reminders", "Projects"}

# Folders where each file is a standalone document
INDIVIDUAL_FOLDERS = {"Meetings", "General_Notes"}

_DATE_RE = re.compile(r"##\s+(\d{4}-\d{2}-\d{2})")


def _extract_date(text: str) -> str:
    m = _DATE_RE.search(text)
    return m.group(1) if m else ""


def load_chunks(kb_dir: Path) -> List[Dict]:
    """
    Read all .md files from kb_dir and return a list of chunks.

    Each chunk is:
        {
            "text":     str,
            "source":   str,   # relative path from kb_dir
            "category": str,   # folder name
            "date":     str,   # YYYY-MM-DD or ""
        }
    """
    chunks: List[Dict] = []

    for folder in kb_dir.iterdir():
        if not folder.is_dir():
            continue

        category = folder.name

        if category in ACCUMULATIVE_FOLDERS:
            # One accumulative file — split by entry separator
            for md_file in folder.glob("*.md"):
                content = md_file.read_text(encoding="utf-8")
                parts = re.split(r"\n---\n\n", content)
                for part in parts:
                    part = part.strip()
                    if len(part) < 40:
                        continue
                    chunks.append({
                        "text":     part,
                        "source":   str(md_file.relative_to(kb_dir)),
                        "category": category,
                        "date":     _extract_date(part),
                    })

        elif category in INDIVIDUAL_FOLDERS:
            # One file per entry — use whole file as one chunk
            for md_file in folder.glob("*.md"):
                content = md_file.read_text(encoding="utf-8").strip()
                if len(content) < 40:
                    continue
                chunks.append({
                    "text":     content,
                    "source":   str(md_file.relative_to(kb_dir)),
                    "category": category,
                    "date":     _extract_date(content),
                })

    return chunks
