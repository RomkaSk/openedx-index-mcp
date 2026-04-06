"""
Documentation index for Open edX sources.

Scans all RST/MD files, classifies them by type (ADR, how-to, reference, etc.),
extracts titles from headings, and caches the result for fast lookups.
"""

import logging
import os
import re
from typing import Optional

from .. import settings

logger = logging.getLogger(__name__)

DOC_EXTENSIONS = {".rst", ".md"}

# RST underline characters (any of these repeated 3+ times)
_RST_UNDERLINE_RE = re.compile(r"^[=\-~`#\"^+*:.]{3,}$")


def _detect_doc_type(path: str) -> Optional[str]:
    """Classify a doc file by its path. Returns None if not a doc file."""
    lower = path.lower()
    basename = os.path.basename(lower)

    # READMEs anywhere
    if basename.startswith("readme."):
        return "readme"

    # CHANGELOGs/HISTORYs anywhere
    if basename.startswith(("changelog.", "history.", "changes.")):
        return "changelog"

    # Path-based classification (must be in a docs-like directory)
    parts = lower.split("/")

    if "decisions" in parts or "adr" in parts:
        return "adr"
    if "how_tos" in parts or "how-tos" in parts:
        return "how-to"
    if "references" in parts or "reference" in parts:
        return "reference"

    # Any other file inside a docs/ directory
    if "docs" in parts or "doc" in parts:
        return "guide"

    return None


def _extract_repo(path: str) -> str:
    """Extract 'category/repo-name' from path like 'core-libraries/openedx-events/...'."""
    parts = path.split("/")
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return parts[0] if parts else ""


def _extract_title(full_path: str) -> str:
    """Extract title from first heading in RST or MD file."""
    try:
        with open(full_path, encoding="utf-8", errors="replace") as f:
            lines = []
            for _ in range(20):  # Read first 20 lines max
                line = f.readline()
                if not line:
                    break
                lines.append(line.rstrip())
    except (OSError, IOError):
        return _title_from_filename(full_path)

    if full_path.endswith(".md"):
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
        return _title_from_filename(full_path)

    # RST: look for a line followed by an underline
    for i in range(len(lines) - 1):
        current = lines[i].strip()
        next_line = lines[i + 1]
        if current and _RST_UNDERLINE_RE.match(next_line) and len(next_line) >= len(current):
            return current
    return _title_from_filename(full_path)


def _title_from_filename(path: str) -> str:
    """Fallback: derive title from filename."""
    name = os.path.splitext(os.path.basename(path))[0]
    # Strip leading numbers like "0002-"
    name = re.sub(r"^\d+-", "", name)
    return name.replace("-", " ").replace("_", " ").strip().title()


# Module-level cache
_docs_cache: Optional[list[dict]] = None


def get_docs_index() -> list[dict]:
    """
    Return cached docs index. Builds on first call.

    Each entry: {"path": str, "title": str, "doc_type": str, "repo": str}
    """
    global _docs_cache
    if _docs_cache is not None:
        return _docs_cache

    _docs_cache = _build_docs_index()
    return _docs_cache


def _build_docs_index() -> list[dict]:
    """Scan all RST/MD files and build metadata index.

    Uses os.walk instead of the shallow index because code-index-mcp's
    shallow index only tracks code files, not documentation.
    """
    sources_dir = os.path.abspath(settings.SOURCES_DIR)

    docs = []
    for root, _dirs, files in os.walk(sources_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in DOC_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, sources_dir)

            doc_type = _detect_doc_type(rel_path)
            if doc_type is None:
                continue

            title = _extract_title(full_path)
            repo = _extract_repo(rel_path)

            docs.append({
                "path": rel_path,
            "title": title,
            "doc_type": doc_type,
            "repo": repo,
        })

    logger.info(f"Docs index built: {len(docs)} documents")
    return docs
